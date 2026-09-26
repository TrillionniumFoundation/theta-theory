#!/usr/bin/env python3
"""Build complete A2 v170 manuscripts from the hash-locked complete v169 sources."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
from frontmatter_v170 import TITLE, II_ABSTRACT, II_INTRO, I_ADD, BIB
from responses_v170 import write_responses
HERE=Path(__file__).resolve().parent
BRANCH='revision/a2-v170-ramified-contact-boundary-2026-09-26'
PREDECESSOR_COMMIT='81e0870e31078a3aaac6006b676ca54667e6d77a'
REVIEW='f50f6a7b194adbb42813988d3e68a43d71ccc520'
FIRST_REVIEW='be1987dd1a37064c0bea291d7ad38ccd12cc5951'
REPORT_BLOB='f84656b9a3b0a6be81b844b21b73efafe08c6d8a'
FIRST_BLOB='b0523d8e6b294379de5a2679c116528063efc014'
REL='papers/A2-v17-boundary-information-coarsening/article/v170'
PINS={
 'geometry':'625f87d0c6c90e04b2b008ab402822556eb63f4e1c1aa7bbade33894f63d2c47',
 'reconstruction':'2933306c04d075687d9bc6393aa9d618788c98cfe0b016c57f04e97904747295',
 'divisor-geometry':'fabe3afedad0e09c0677ed1686516cccfe5709c4c1d4f42a4a6638a565b5e852'}
PARTS=['ramified-boundary-v170.tex','conductors-and-lifts-v170.tex']
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


def assemble(prev:Path):
 old={};templates={}
 for name,pin in PINS.items():
  p=prev/(name+'.tex');require(p.is_file() and sha(p)==pin,'Wrong complete v169 source: '+name)
  old[name]=p.read_text();s=strip_embedded(old[name])
  sections=list(SEC.finditer(s));end=sections[1].start() if name!='geometry' else sections[0].start()
  (HERE/('PREVIOUS_'+name.upper().replace('-','_')+'_FRONTMATTER_V169.tex')).write_text(s[:end])
  templates[name]=s.replace('revision 169}', 'revision 170}',1)
 parts='\n'.join((HERE/n).read_text() for n in PARTS)
 anchor=r'\section{Coordinate descent and comparisons of compactifications}'
 templates['geometry']=once(templates['geometry'],anchor,parts+'\n'+anchor)
 s=templates['divisor-geometry'];s=once(s,anchor,parts+'\n'+anchor)
 s=abstract(s,II_ABSTRACT)
 sections=list(SEC.finditer(s));require(sections[0].group(1)=='Introduction','Introduction missing')
 s=s[:sections[0].start()]+II_INTRO+'\n'+s[sections[1].start():]
 s=s.replace('Primitive graph ideals and higher-contact Hilbert limits',TITLE)
 templates['divisor-geometry']=s
 anchor=r'\section{First relations, ungraded isomorphisms, and inverse systems}'
 templates['reconstruction']=once(templates['reconstruction'],anchor,I_ADD+'\n'+anchor)
 templates['geometry']=once(templates['geometry'],r'\end{abstract}',
 'The normalization, full parameter fibre, global conductor, and root-label\nidentifications of every marked coefficient cover are included as well.\n'+r'\end{abstract}')
 disclosure=r"""
\paragraph{Revision 170.}
AI assistance was used in deriving and drafting the ramified parameter-fibre,
conductor, and normalization-label arguments and in preparing auxiliary
exact checks. The written proofs are submitted for independent scrutiny.
Compilation, finite checks, and source preservation are not represented as
an external proof audit, a formal proof certificate, or a journal endorsement.
"""
 for name,s in templates.items():
  s=once(s,r'\begin{thebibliography}',disclosure+'\n'+r'\begin{thebibliography}')
  templates[name]=once(s,r'\end{thebibliography}',BIB+'\n'+r'\end{thebibliography}')
 original=counts(old['geometry']);current=counts(templates['geometry'])
 require(not(original-current),'An inherited proof or statement changed')
 require(current==counts(templates['reconstruction'])+counts(templates['divisor-geometry']),'Pair does not partition master')
 labels=LABEL.findall(templates['geometry']);previous=LABEL.findall(old['geometry'])
 missing=sorted(set(previous)-set(labels));dups=sorted(k for k,v in collections.Counter(labels).items() if v>1)
 require(not missing and not dups,'Missing or duplicate labels in master')
 available=set().union(*(set(LABEL.findall(s)) for s in templates.values()))
 for name,s in templates.items():
  require(not(set(REF.findall(s))-available),'Unknown refs in '+name+': '+str(set(REF.findall(s))-available))
  own=LABEL.findall(s);require(len(own)==len(set(own)),'Duplicate labels '+name)
  require(not(counts(old[name])-counts(s)),'Per-paper block retention failed '+name)
  (HERE/(name+'.tex')).write_text(s)
 receipt={'revision':170,'complete_predecessor_commit':PREDECESSOR_COMMIT,
 'controlling_review_commit':REVIEW,'earlier_review_commit':FIRST_REVIEW,
 'predecessor_sha256':PINS,'predecessor_math_blocks':sum(original.values()),
 'current_math_blocks':sum(current.values()),'predecessor_labels':len(previous),'current_labels':len(labels),
 'missing_labels':missing,'duplicate_labels':dups,'all_predecessor_math_blocks_retained_byte_for_byte':True,
 'per_paper_math_blocks_retained':True,'body_partitioned_exactly_once':True,
 'all_three_predecessor_frontmatters_archived':True,'historical_manuscript_sources_modified':False,
 'external_independent_paper_I_audit_obtained':False,
 'new_classification_domain':'All a>=2 and rho,sigma>=1 of the marked ramified family; not every fibre of full B_a.'}
 require(receipt['predecessor_math_blocks']==465 and receipt['predecessor_labels']==682,'Unexpected predecessor counts')
 (HERE/'NONDELETION_V170.json').write_text(json.dumps(receipt,indent=2)+'\n')
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
 lines=['% BEGIN V170 COMPANION REFERENCES','\\makeatletter']
 for k in needed:
  n,p=other[k];lines.append('\\@namedef{r@'+k+'}{{'+prefix+'.'+n+'}{'+prefix+'.'+p+'}{}{}{}}')
 lines+=['\\makeatother','% END V170 COMPANION REFERENCES']
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
 (HERE/'THEOREM_INDEX_V170.json').write_text(json.dumps(index,indent=2)+'\n')
 render=HERE/'render-audit';render.mkdir(exist_ok=True)
 selected={'reconstruction':{1},'divisor-geometry':{1},'geometry':{1}}
 for key,rec in index.items():
  if key.endswith('v170') and key.startswith(('thm:','prop:','lem:','cor:','ex:')):
   name=rec['paper'];p=int(rec['page']);selected[name].update(range(p,min(p+2,outputs[name]['pages'])+1))
 for name,pages in selected.items():
  for page in sorted(pages):subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1400','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
 return outputs,{n:sorted(p) for n,p in selected.items()}


def response_crosswalk():
 index=json.loads((HERE/'THEOREM_INDEX_V170.json').read_text());text='# A2 v170 — compiled referee locators\n\n'
 for source in ('RESPONSE_TO_SECOND_V167_REPORT.md','RESPONSE_TO_FIRST_V167_REPORT.md'):
  text+='## '+source+'\n\n'
  for item in re.split(r'(?=^### \d+\.)',(HERE/source).read_text(),flags=re.M)[1:]:
   heading=item.splitlines()[0][4:];keys=sorted(set(re.findall(r'(?:thm|prop|cor|lem|eq|sec|ex):[a-zA-Z0-9-]+',item)))
   entries=[]
   for key in keys:
    if key not in index:continue
    r=index[key];entries.append(f'`{key}`: {r["paper"]}, {r["number"]}, p. {r["page"]} (master p. {r.get("master_page","n/a")})')
   text+='### '+heading+'\n\n'+('; '.join(entries) if entries else 'See the response text and its stated scope/documentary status.')+'\n\n'
 (HERE/'REFEREE_CROSSWALK_V170.md').write_text(text)


def publish(root:Path,receipt:dict):
 text=f'''# A2 revision 170 — complete referee entry

Branch: `{BRANCH}`.

Complete predecessor: `{PREDECESSOR_COMMIT}` (v169).

Latest controlling review: `{REVIEW}` (second v167 report).

Earlier v167 report: `{FIRST_REVIEW}`.

Authored build commit: `{receipt['source_commit']}`.

'''
 titles={'reconstruction':'Paper I — Finite failure schemes and the reconstruction of quadratic pencils','divisor-geometry':'Paper II — '+TITLE,'geometry':'Complete preservation master — not a third submission'}
 for n,title in titles.items():
  text+=f'## {title}\n\n{receipt["outputs"][n]["pages"]} pages. [Complete PDF]({REL}/{n}.pdf) · [Standalone LaTeX]({REL}/{n}.tex).\n\n'
 text+='''## New mathematics relative to the complete v169 package

For every contact order a>=2 and every coefficient cover b=u^rho,c=v^sigma,
the revision determines the full integral Hilbert graph, its normalized Rees
algebra in all degrees, every cyclic quotient chart, and the complete scheme
fibre of the normalized parameter surface. With g_i=gcd(rho,i sigma), the
primitive rays are (i sigma/g_i,rho/g_i); the fibre has lengths
min(rho,i sigma)/g_i, no embedded points, and the exact maximum nilpotence
order. Its reduced boundary is a nodal chain of a rational curves.

The global conductor ideal has orders
(rho i sigma-rho-i sigma)/g_i+1. A depth lemma excludes any extra condition
at crossings. On each open boundary orbit the normalized residue coordinate
maps to its g_i-th power: all the lost root labels are realized by actual
arcs. Equal-power covers have explicit conductor generators on every chart.
The models are compatible with successive root covers and marked Cartier
boundary trivializations. A separate corollary describes the scheme fibre
of any normal toric surface modification of the plane, without Paper I.

'''
 text+=f'All {receipt["predecessor_math_blocks"]} v169 mathematical blocks and {receipt["predecessor_labels"]} master labels are retained. No historical manuscript source is modified. Complete predecessor front matters are archived; the two paper bodies partition the master exactly.\n\n'
 for n,title in [('RESPONSE_TO_SECOND_V167_REPORT.md','All 66 controlling requests with v170 amendments'),('RESPONSE_TO_FIRST_V167_REPORT.md','All 66 earlier requests and inherited responses'),('REFEREE_CROSSWALK_V170.md','Actual compiled theorem and page locators'),('THEOREM_DEPENDENCIES_V170.md','Proof dependencies and publication units'),('THEOREM_INDEX_V170.json','Complete compiled theorem index'),('BUILD_RECEIPT_V170.json','Build and source-hash receipt'),('NONDELETION_V170.json','Byte-level proof preservation'),('EXACT_CHECKS_V170.json','Auxiliary exact checks'),('LITERATURE_AUDIT_V170.md','Primary sources and documentary scope')]:
  text+=f'[{title}]({REL}/{n})\n\n'
 text+='''## Scope and audit status

The complete parameter-fibre classification is for the stated marked
ramified family, not the full B_3 or B_a fibre or all higher-corank and
singular-pencil strata. Root-cover compatibility does not assert gluing
across different generic Hilbert polynomials. Normalizing parameters does
not normalize the universal embedded curves. The effective failure-algebra
application still reconstructs the specified family first.

No external independent full proof audit of Paper I or complete Ballico 1993
theorem/proof comparison was obtained. The checked mathematical arguments
are offered for re-review; auxiliary finite checks and compilation are not
proof, originality, or journal-acceptance certificates. Both review branches,
v168, v169, and all earlier revision branches remain untouched.
'''
 for name in ('CURRENT_REVIEW_ENTRY.md','README.md'):
  p=root/name;arch=HERE/('PREVIOUS_ROOT_'+name.replace('.md','')+'_V169.md')
  if p.exists() and not arch.exists():shutil.copyfile(p,arch)
 (root/'CURRENT_REVIEW_ENTRY.md').write_text(text)
 (root/'A2_REVISION_V170_INDEX.md').write_text(text)
 (root/'README.md').write_text('# Theta-Theory — A2 revision 170\n\n[Current referee entry](CURRENT_REVIEW_ENTRY.md) provides the complete manuscript PDFs, standalone sources, both itemwise referee responses, compiled theorem locators, proof preservation, and actual build receipts.\n\nThis new branch builds on the complete v169 package and adds the all-order ramified-boundary and conductor theorem. Earlier revisions and reviews are preserved.\n')
 (HERE/'CURRENT_REVIEW_ENTRY.md').write_text(text.replace(REL+'/',''))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true')
 ap.add_argument('--baseline',type=Path,default=HERE.parent/'v169')
 ap.add_argument('--root',type=Path,default=HERE.parents[3])
 args=ap.parse_args();args.root.mkdir(parents=True,exist_ok=True)
 for name in ('LITERATURE_AUDIT_V169.md','THEOREM_DEPENDENCIES_V169.md','BUILD_RECEIPT_V169.json','NONDELETION_V169.json'):
  src=args.baseline/name
  require(src.is_file(),'Missing predecessor audit material: '+name)
  shutil.copyfile(src,HERE/('INHERITED_'+name))
 validated={}
 for key,name,expected in [('second','CONTROLLING_SECOND_V167_REPORT.md',REPORT_BLOB),('first','EARLIER_FIRST_V167_REPORT.md',FIRST_BLOB)]:
  p=args.baseline/name;require(p.is_file(),'Missing inherited exact report: '+name)
  b=p.read_bytes();digest=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  require(digest==expected,'Wrong controlling report bytes: '+key)
  (HERE/name).write_bytes(b);validated[key]=True
 write_responses(HERE,args.baseline)
 for name in ('RESPONSE_TO_SECOND_V167_REPORT.md','RESPONSE_TO_FIRST_V167_REPORT.md'):
  require(list(map(int,re.findall(r'^### (\d+)\.',(HERE/name).read_text(),re.M)))==list(range(1,67)),'Incomplete responses '+name)
 templates,receipt=assemble(args.baseline)
 receipt.update(source_commit=os.environ.get('GITHUB_SHA','local-prepublication-audit'),report_blob_locks={'second':REPORT_BLOB,'first':FIRST_BLOB},report_bytes_validated=validated,compiled=False)
 if args.build:
  checks=json.loads((HERE/'EXACT_CHECKS_V170.json').read_text());require(checks['all_checks_pass'],'Run exact checks first')
  for name,digest in checks['source_sha256'].items():require(sha(HERE/name)==digest,'Tests are not for current mathematical sources: '+name)
  if os.environ.get('GITHUB_ACTIONS'):require(checks['inherited_v169_full_chain_rerun'],'Remote publication requires all inherited checks')
  outputs,rendered=build(templates)
  receipt.update(compiled=True,outputs=outputs,rendered_pages=rendered,companion_references_stabilized=True,inherited_v169_full_chain_rerun=checks['inherited_v169_full_chain_rerun'])
  response_crosswalk();publish(args.root,receipt)
 (HERE/'BUILD_RECEIPT_V170.json').write_text(json.dumps(receipt,indent=2)+'\n')
 manifest={p.name:sha(p) for p in HERE.iterdir() if p.suffix in ('.py','.tex','.md') and not p.name.startswith(('PREVIOUS_','geometry','reconstruction','divisor-geometry','CURRENT_REVIEW_ENTRY'))}
 (HERE/'SOURCE_MANIFEST_V170.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for name,pin in PINS.items():require(sha(args.baseline/(name+'.tex'))==pin,'Predecessor source changed')
 print(json.dumps({'compiled':receipt['compiled'],'retained_blocks':receipt['predecessor_math_blocks'],'current_blocks':receipt['current_math_blocks'],'outputs':receipt.get('outputs',{})},indent=2))
if __name__=='__main__':main()
