#!/usr/bin/env python3
"""Assemble complete v166 manuscripts, preserve all v164 proofs, and compile.

No historical source is edited. Run from the repository with --build.
The optional --baseline and --root arguments support a local artifact audit.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
from frontmatter_v166 import II_ABSTRACT, II_INTRO, I_ADD, BIB
HERE=Path(__file__).resolve().parent
BRANCH='revision/a2-v166-universal-flattening-2026-09-26'
REVIEW='e795bc76e458260f0efcc8182c292f19d0610ca0'
REPORT_BLOB='9c1b6c09e6bddf67bdd97d3066638ea33bf4348b'
REL='papers/A2-v17-boundary-information-coarsening/article/v166'
PINS={
 'geometry':'92d97cc1d0c97ebc324e12717b8c57fd53450bcd225b3d8eac167bda5a91bae2',
 'reconstruction':'f267fc7ac13451657712d0ca37ee1145e35a2a0950515926772d290ebe86ed6a',
 'divisor-geometry':'824e2b6906b635cfe4b92f27076fd0dca788f0919a589887c2c27c2c94f08082'}
PARTS=['horizontal-flattening-v166.tex','miniversal-specialization-v166.tex',
       'extension-and-ramification-v166.tex','comparison-details-v166.tex',
       'effective-horizontal-v166.tex']
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
 parts={n:(HERE/n).read_text() for n in PARTS}
 for name,s in old.items():
  matches=list(SEC.finditer(s))
  end=matches[1].start() if name!='geometry' else matches[0].start()
  (HERE/('PREVIOUS_'+name.upper().replace('-','_')+'_FRONTMATTER_V164.tex')).write_text(s[:end])
 templates={n:strip_embedded(s).replace('revision 164}', 'revision 166}',1) for n,s in old.items()}
 s=templates['reconstruction']
 s=once(s,'\\label{sec:paper-i-v164}','\\label{sec:paper-i-v164}\\label{sec:paper-i-v166}')
 s=once(s,'\\section{First relations, ungraded isomorphisms, and inverse systems}',I_ADD+'\n\\section{First relations, ungraded isomorphisms, and inverse systems}')
 s=once(s,'\\end{abstract}','Universal horizontal specialization and the nonsplit contact-fibre\nalgebra extend this effective geometric application.\n\\end{abstract}')
 s=once(s,'\\begin{thebibliography}',parts[PARTS[4]]+'\n\\begin{thebibliography}')
 templates['reconstruction']=s
 s=templates['divisor-geometry'];s=abstract(s,II_ABSTRACT)
 a,b=section_span(s,'Introduction');s=s[:a]+II_INTRO+'\n'+s[b:]
 a,b=section_span(s,'Quadratic sections of reciprocal normalization fibres');moved=s[a:b];s=s[:a]+s[b:]
 s=once(s,'\\section{Power coefficients and their twists}',parts[PARTS[0]]+'\n\\section{Power coefficients and their twists}')
 s=once(s,'\\section{Collision of two incidence points}',parts[PARTS[1]]+'\n\\section{Collision of two incidence points}')
 s=once(s,'\\section{Products and adjacency for the first nonreduced boundary}',parts[PARTS[2]]+'\n\\section{Products and adjacency for the first nonreduced boundary}')
 app='\\appendix\n\\renewcommand{\\thesection}{\\AlphAlph{\\value{section}}}\n'
 s=once(s,app,app+parts[PARTS[3]]+'\n'+moved+'\n')
 templates['divisor-geometry']=s
 s=templates['geometry']
 newmain='\n'.join(parts[n] for n in (PARTS[0],PARTS[1],PARTS[2],PARTS[4]))
 s=once(s,'\\appendix',newmain+'\n\\appendix\n'+parts[PARTS[3]])
 s=once(s,'\\end{abstract}','Universal horizontal models, all-arc double-contact presentations,\nthe nonsplit algebra extension, and arbitrary ramification are\nproved in the additional sections.\n\\end{abstract}')
 s=once(s,'\\section{First relations, ungraded isomorphisms, and inverse systems}',r'''\subsection{Universal horizontal specialization}
The new primary results are Theorems~\ref{thm:horizontal-universal-v166},
\ref{thm:all-arcs-v166}, \ref{thm:extension-class-v166}, and
\ref{thm:ramified-v166}. The complete companion papers supply their
focused reading order; this master retains every preceding proof.
\section{First relations, ungraded isomorphisms, and inverse systems}''')
 templates['geometry']=s
 for name,s in templates.items():
  templates[name]=once(s,'\\end{thebibliography}',BIB+'\n\\end{thebibliography}')
 original=counts(old['geometry']);current=counts(templates['geometry'])
 pair=counts(templates['reconstruction'])+counts(templates['divisor-geometry'])
 oldlabels=LABEL.findall(old['geometry']);newlabels=LABEL.findall(templates['geometry'])
 require(len(oldlabels)==539 and sum(original.values())==358,'Unexpected predecessor counts')
 require(not(original-current),'A previous mathematical block was changed or removed')
 require(current==pair,'Mathematical blocks must partition exactly once between the two papers')
 missing=sorted(set(oldlabels)-set(newlabels))
 duplicates=sorted(k for k,v in collections.Counter(newlabels).items() if v>1)
 require(not missing and not duplicates,'Missing or duplicate master labels')
 available=set().union(*(set(LABEL.findall(s)) for s in templates.values()))
 for name,s in templates.items():
  require(not(set(REF.findall(s))-available),'Unknown reference in '+name+': '+str(set(REF.findall(s))-available))
  own=LABEL.findall(s);require(len(own)==len(set(own)),'Duplicate labels in '+name)
  for block,count in counts(old[name]).items():require(counts(s)[block]>=count,'Nondeletion failure in '+name)
  (HERE/(name+'.tex')).write_text(s)
 receipt={'revision':166,'controlling_review_commit':REVIEW,'predecessor_sha256':PINS,
 'predecessor_labels':len(oldlabels),'current_labels':len(newlabels),
 'predecessor_math_blocks':sum(original.values()),'current_math_blocks':sum(current.values()),
 'missing_labels':missing,'duplicate_labels':duplicates,
 'all_predecessor_math_blocks_retained_byte_for_byte':True,'body_partitioned_exactly_once':True,
 'all_three_predecessor_frontmatters_archived':True,'historical_manuscript_sources_modified':False,
 'moved_intact_to_appendix':['Quadratic sections of reciprocal normalization fibres'],
 'external_independent_paper_I_audit_obtained':False}
 (HERE/'NONDELETION_V166.json').write_text(json.dumps(receipt,indent=2)+'\n')
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
 lines=['% BEGIN V166 COMPANION REFERENCES','\\makeatletter']
 for k in needed:
  n,p=other[k];lines.append('\\@namedef{r@'+k+'}{{'+prefix+'.'+n+'}{'+prefix+'.'+p+'}{}{}{}}')
 lines+=['\\makeatother','% END V166 COMPANION REFERENCES']
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
 (HERE/'THEOREM_INDEX_V166.json').write_text(json.dumps(index,indent=2)+'\n')
 render=HERE/'render-audit';render.mkdir(exist_ok=True)
 selected={'reconstruction':{1},'divisor-geometry':{1},'geometry':{1}}
 for key,rec in index.items():
  if key.endswith('v166') and key.startswith(('thm:','prop:')):
   name=rec['paper'];p=int(rec['page']);selected[name].update(range(p,min(p+2,outputs[name]['pages'])+1))
 for name,pages in selected.items():
  for page in sorted(pages):subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1400','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
 return outputs,{n:sorted(p) for n,p in selected.items()}

def publish(root:Path,receipt:dict):
 for name in ['CURRENT_REVIEW_ENTRY.md','README.md']:
  p=root/name;archive=HERE/('PREVIOUS_ROOT_'+name)
  if p.exists() and not archive.exists():shutil.copyfile(p,archive)
 text='# A2 revision 166 — current review entry\n\n'
 text+=f'Branch: `{BRANCH}`.\n\nControlling referee commit: `{REVIEW}`.\n\nAuthored build source commit: `{receipt["source_commit"]}`.\n\n'
 titles={'reconstruction':'Paper I — Finite failure schemes and the reconstruction of quadratic pencils','divisor-geometry':'Paper II — Power ideals and the Hilbert boundary of quadratic pencils','geometry':'Complete preservation master (not a third submission)'}
 for n,title in titles.items():
  text+=f'## {title}\n\n{receipt["outputs"][n]["pages"]} pages. [Complete PDF]({REL}/{n}.pdf) · [Standalone complete LaTeX]({REL}/{n}.tex).\n\n'
 text+='''## Main additions

Universal horizontal modifications with a stratumwise lifting property;
seven retained-coefficient presentations for all discrete valuation ring
arcs through the double contact; the nonsplit square-zero extension and
its obstruction sheaf on the doubled-line curve; realization of every
conic by coefficient arcs; arbitrary ramification, cyclic-invariant
normalization, and the complete vertical torsion filtration.

The relative-Hilbert representability construction is classical and is
attributed. Its application does not claim an explicit classification
of all higher-contact components. The effective failure-family
application still uses the sharp reconstruction theorem.

'''
 for n,title in [('RESPONSE_TO_V164_REPORT.md','All 54 referee responses'),('THEOREM_INDEX_V166.json','Compiled theorem and page index'),('BUILD_RECEIPT_V166.json','Compilation and source receipt'),('NONDELETION_V166.json','Byte-for-byte proof retention'),('EXACT_CHECKS_V166.json','Exact algebra checks'),('LITERATURE_AUDIT_V166.md','Primary-source and documentary audit'),('PAPER_I_AUDIT_HANDOFF.md','Independent-audit handoff')]:text+=f'[{title}]({REL}/{n})\n\n'
 text+='''## Scope and external obligations

All previous mathematical blocks are retained. The full v164 review is
copied into the revision directory and remains unchanged at its original
path. Main and review branches are not publication targets. The v165
branch alias was not treated as a new manuscript.

No external independent full audit of Paper I was obtained, and the
Ballico 1993 full text was not retrieved. Neither fact is represented as
completed. Finite computations and a clean PDF build are not proofs of
the general theorems, novelty, or journal acceptance.
'''
 (root/'CURRENT_REVIEW_ENTRY.md').write_text(text);(HERE/'CURRENT_REVIEW_ENTRY.md').write_text(text.replace(REL+'/', ''))
 (root/'README.md').write_text('# Theta-Theory — A2 revision 166\n\nThis revision branch contains complete new A2 manuscripts prepared against the locked v164 referee report.\n\n[Current review entry](CURRENT_REVIEW_ENTRY.md) provides the complete papers, response, and verification receipts.\n\nThe original repository README is preserved at ['+REL+'/PREVIOUS_ROOT_README.md]('+REL+'/PREVIOUS_ROOT_README.md). Historical sources, other papers, and the controlling review are retained.\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--baseline',type=Path,default=HERE.parent/'v164');ap.add_argument('--root',type=Path,default=HERE.parents[3]);args=ap.parse_args()
 args.root.mkdir(parents=True,exist_ok=True)
 report=args.root/'reviews/a2-v164-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md'
 if not report.exists():report=HERE/'CONTROLLING_REFEREE_REPORT_V164.md'
 data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 require(blob==REPORT_BLOB,'Wrong controlling referee report')
 (HERE/'CONTROLLING_REFEREE_REPORT_V164.md').write_bytes(data)
 response=(HERE/'RESPONSE_TO_V164_REPORT.md').read_text()
 require(list(map(int,re.findall(r'^### (\d+)\.',response,re.M)))==list(range(1,55)),'All 54 responses are required')
 templates,receipt=assemble(args.baseline)
 receipt.update(source_commit=os.environ.get('GITHUB_SHA','local-artifact-audit'),controlling_report_blob=blob,compiled=False)
 if args.build:
  outputs,rendered=build(templates);receipt.update(compiled=True,outputs=outputs,rendered_pages=rendered,companion_references_stabilized=True)
  check=json.loads((HERE/'EXACT_CHECKS_V166.json').read_text());require(check['all_checks_pass'],'Exact checks required')
  receipt['inherited_v164_suite_rerun']=check['inherited_v164_suite_rerun']
  publish(args.root,receipt)
 manifest={p.name:sha(p) for p in HERE.iterdir() if p.suffix in ('.py','.tex','.md') and not p.name.startswith(('PREVIOUS_','geometry','reconstruction','divisor-geometry','CURRENT_REVIEW_ENTRY'))}
 (HERE/'SOURCE_MANIFEST_V166.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (HERE/'BUILD_RECEIPT_V166.json').write_text(json.dumps(receipt,indent=2)+'\n')
 for name,pin in PINS.items():require(sha(args.baseline/(name+'.tex'))==pin,'Historical manuscript was modified')
 print(json.dumps({'compiled':receipt['compiled'],'retained_blocks':358,'retained_labels':539,'outputs':receipt.get('outputs',{})},indent=2))
if __name__=='__main__':main()
