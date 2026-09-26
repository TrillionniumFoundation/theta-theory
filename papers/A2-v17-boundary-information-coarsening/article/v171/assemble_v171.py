#!/usr/bin/env python3
"""Build publication papers and complete nondeleted archive from locked v170 sources."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
from frontmatter_v171 import TITLE, ABSTRACT, INTRO, I_INTRO, ACK, BIB
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BRANCH='revision/a2-v171-duality-conductor-base-change-2026-09-27'
REVIEW='35b33cd5b0eda133137c9baa7e2a1ef0591dc58b'
REPORT_PATH='reviews/a2-v170-independent-harsh-top4-2026-09-27/REFEREE_REPORT.md'
REPORT_BLOB='94fe39b7a97b20324ac45aa6b38b43297e87ca01'
PREDECESSOR='b8c3c1d7e59591b4e402272773d9bed5ae7c88ba'
REL='papers/A2-v17-boundary-information-coarsening/article/v171'
PINS={'geometry':'38d9e245676223d2e875f6a663826143a12b7021af1fa3fb0d750d259c77cee9',
      'reconstruction':'b28e92c277925ea9a03e3fc89d7f8e31885ce0cebecf78e85e28c9b364fd97d5',
      'divisor-geometry':'23bf51db6fd60b9143f68ffa0e681c2a2917967ebc49c2a396307e6f39d6f727'}
PARTS=['duality-base-change-v171.tex','self-contained-chain-v171.tex',
       'tangent-covers-v171.tex','diagonal-proof-completion-v171.tex']
MATH=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|remark|example|definition|proof)\}.*?\\end\{\1\}',re.S)
LABEL=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}')
AUX=re.compile(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}')
SEC=re.compile(r'\\section\{([^}]+)\}')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def counts(s):return collections.Counter(hashlib.sha256(m.group().encode()).hexdigest() for m in MATH.finditer(s))
def strip_refs(s):return re.sub(r'% BEGIN V\d+ COMPANION REFERENCES\n.*?% END V\d+ COMPANION REFERENCES\n','',s,flags=re.S)
def replace_abstract(s,text):return re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:'\\begin{abstract}\n'+text.strip()+'\n\\end{abstract}',s,count=1,flags=re.S)
def deterministic(s):
    if '\\usepackage{alphalph}' not in s:s=s.replace('\\begin{document}','\\usepackage{alphalph}\n\\begin{document}',1)
    s=s.replace('\\begin{document}','\\pdfinfoomitdate=1\n\\pdftrailerid{}\n\\begin{document}',1)
    if '\\AlphAlph' not in s:s=s.replace('\\appendix','\\appendix\n\\renewcommand{\\thesection}{\\AlphAlph{\\value{section}}}',1)
    return s

def assemble():
    prev=HERE.parent/'v170';old={}
    for n,pin in PINS.items():
        require(sha(prev/(n+'.tex'))==pin,'Wrong predecessor source '+n)
        old[n]=(prev/(n+'.tex')).read_text()
    report=(ROOT/REPORT_PATH).read_bytes()
    require(hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest()==REPORT_BLOB,'Wrong report')
    (HERE/'CONTROLLING_REFEREE_REPORT_V170.md').write_bytes(report)
    header=strip_refs(old['divisor-geometry']).split('\\begin{document}')[0]
    sections={n:list(SEC.finditer(strip_refs(s))) for n,s in old.items()}
    for n,s in old.items():
        text=strip_refs(s);cut=sections[n][0 if n=='geometry' else 1].start()
        (HERE/('ARCHIVED_'+n.upper().replace('-','_')+'_FRONTMATTER_V170.tex')).write_text(text[:cut])
    parts='\n\n'.join((HERE/n).read_text() for n in PARTS)
    newmain=header+'\\begin{document}\n\\title{'+TITLE+'}\n\\author{Qian Qi}\n\\date{September 27, 2026}\n'
    newmain+='\\subjclass[2020]{14B05, 14D20, 13B22, 14M25}\n\\hypersetup{pdftitle={'+TITLE+'},pdfauthor={Qian Qi}}\n'
    newmain+='\\begin{abstract}\n'+ABSTRACT.strip()+'\n\\end{abstract}\n\\maketitle\n'+INTRO+'\n'+parts+'\n'+ACK
    newmain+='\n\\begin{thebibliography}{99}\n'+BIB+'\n\\end{thebibliography}\n\\end{document}\n'

    # Active Paper I: replace only its nonmathematical introductory survey and disclosures.
    paperI=strip_refs(old['reconstruction']);ss=list(SEC.finditer(paperI))
    paperI=paperI[:ss[0].start()]+I_INTRO+'\n'+paperI[ss[1].start():]
    start=paperI.index('\\section*{Acknowledgment of assistance}')
    end=paperI.index('\\section{Universal horizontal families on the effective image}',start)
    (HERE/'ARCHIVED_ASSISTANCE_DISCLOSURES_V170.tex').write_text(paperI[start:end])
    paperI=paperI[:start]+paperI[end:]
    start=paperI.index('\\paragraph{Revision 169.}')
    end=paperI.index('\\begin{thebibliography}',start)
    (HERE/'ARCHIVED_LATE_DISCLOSURES_V170.tex').write_text(paperI[start:end])
    paperI=paperI[:start]+ACK+'\n'+paperI[end:]
    paperI=paperI.replace('September 26, 2026','September 27, 2026',1)
    paperI=paperI.replace(', revision 170}','}',1)

    # All old Paper II mathematics is a fully typeset technical supplement, not deleted.
    supp=strip_refs(old['divisor-geometry']);ss=list(SEC.finditer(supp))
    old_title='Conductors and ramified Hilbert boundaries of polynomial contacts'
    supp=supp.replace(old_title,'Technical supplement: polynomial-contact Hilbert geometry')
    supp=replace_abstract(supp,'This technical supplement contains the complete preceding mathematical development of polynomial-contact Hilbert graphs, power ideals, equivariant constructions, embedded contact limits, and diagonal ramification. It is a reference companion to the independently readable paper on conductor duality and tangent coefficient changes. All mathematical statements and proofs of the preceding development are retained.')
    ss=list(SEC.finditer(supp));intro='\\section{Guide to the supplement}\n'+''.join('\\label{'+x+'}' for x in LABEL.findall(supp[ss[0].start():ss[1].start()]))+'\n'
    intro+='The central route of the new conductor paper does not depend on this supplement. The full earlier mathematical development is included here for verification and for its applications. Cross-references marked I refer to the reconstruction paper; references without a prefix are internal.\n'
    supp=supp[:ss[0].start()]+intro+supp[ss[1].start():]
    supp=supp.replace('September 26, 2026','September 27, 2026',1).replace(', revision 170}','}',1)

    # The archive master keeps every old mathematical block and adds the entire new route.
    master=strip_refs(old['geometry']);first=list(SEC.finditer(master))[0].start()
    front_labels=LABEL.findall(master[:first])
    master_header=master.split('\\begin{document}')[0]
    master_front=master_header+'\\begin{document}\n\\title[Archival master]{Archival master: reconstruction and coefficient-change Hilbert geometry}\n\\author{Qian Qi}\n\\date{September 27, 2026}\n'
    master_front+='\\hypersetup{pdftitle={Archival master: reconstruction and coefficient-change Hilbert geometry},pdfauthor={Qian Qi}}\n'
    master_front+='\\begin{abstract}This repository archive preserves every mathematical statement and proof from the complete preceding reconstruction and Hilbert-boundary manuscripts and includes the new conductor-duality and tangent-cover arguments. The two publication papers and the complete technical supplement provide separate reading routes. This master is not a third journal submission.\\end{abstract}\n\\maketitle\n'
    master_front+='\\section*{Reading the archive}\n'+''.join('\\label{'+x+'}' for x in front_labels)+'\n'
    master_front+='The earlier mathematical development is retained in full. The final sections present the independently readable conductor and nonmonomial coefficient-change route. Source-history front matters are archived separately. An external independent full audit of the inverse theorem and the complete Ballico 1993 comparison are not represented as completed.\n'
    master=master_front+master[first:]
    master=master.replace('\\begin{thebibliography}','\\clearpage\n'+INTRO+'\n'+parts+'\n\\begin{thebibliography}',1)
    master=master.replace('\\end{thebibliography}',BIB+'\n\\end{thebibliography}',1)
    templates={n:deterministic(s) for n,s in [('reconstruction',paperI),('divisor-geometry',newmain),('technical-supplement',supp),('geometry',master)]}
    oldcount=counts(old['geometry']);newcount=counts(templates['geometry'])
    require(not oldcount-newcount,'Missing predecessor mathematical blocks')
    require(sum(oldcount.values())==487,'Unexpected baseline math count')
    require(newcount==sum((counts(templates[n]) for n in ('reconstruction','divisor-geometry','technical-supplement')),collections.Counter()),'Publication papers and supplement do not partition the archive mathematics')
    require(counts(old['reconstruction'])==counts(templates['reconstruction']),'Paper I mathematical proofbody changed')
    require(counts(old['divisor-geometry'])==counts(templates['technical-supplement']),'Prior Paper II proofbody changed')
    labels=LABEL.findall(templates['geometry']);oldlabels=LABEL.findall(old['geometry'])
    missing=sorted(set(oldlabels)-set(labels));duplicates=[x for x,n in collections.Counter(labels).items() if n>1]
    require(len(oldlabels)==706 and not missing and not duplicates,'Missing or duplicate master labels')
    all_labels=set().union(*(set(LABEL.findall(s)) for s in templates.values()))
    for n,s in templates.items():
        require(not(set(REF.findall(s))-all_labels),'Unknown labels '+n+': '+str(set(REF.findall(s))-all_labels))
        require(len(LABEL.findall(s))==len(set(LABEL.findall(s))),'Duplicate labels '+n)
        (HERE/(n+'.tex')).write_text(s)
    receipt={'revision':171,'controlling_review_commit':REVIEW,'controlling_report_blob':REPORT_BLOB,
             'complete_predecessor_commit':PREDECESSOR,'predecessor_tex_sha256':PINS,
             'predecessor_math_blocks':487,'current_math_blocks':sum(newcount.values()),
             'new_paper_math_blocks':sum(counts(newmain).values()),'predecessor_labels':706,
             'current_labels':len(labels),'missing_labels':missing,'duplicate_labels':duplicates,
             'all_predecessor_math_blocks_retained_byte_for_byte':True,
             'paper_I_proofbody_retained_byte_for_byte':True,
             'paper_II_predecessor_retained_in_complete_supplement':True,
             'papers_plus_supplement_partition_master':True,
             'historical_sources_modified':False,'report_bytes_validated':True,
             'external_independent_paper_I_audit_obtained':False,
             'master_is_archival_not_a_submission':True,'source_commit':os.environ.get('GITHUB_SHA','local-build'),
             'new_claim_domain':'Conductor duality for all normal proper birational models under finite flat smooth covers; full square-tangency surface classification for all contact orders; not a full B_a Hilbert-fibre classification.'}
    (HERE/'NONDELETION_V171.json').write_text(json.dumps({k:v for k,v in receipt.items() if k!='source_commit'},indent=2)+'\n')
    return templates,receipt

def compile_one(name,passes=2):
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790440308',FORCE_SOURCE_DATE='1',TZ='UTC')
    for i in range(passes):
        p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',name+'.tex'],cwd=HERE,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (HERE/(name+'.build-output.txt')).write_text(p.stdout)
        require(p.returncode==0,'LaTeX failed: '+name+'; see build-output')
def aux(name):return {k:(n,p) for k,n,p in AUX.findall((HERE/(name+'.aux')).read_text())}
def embed(s,other,prefix):
    missing=sorted(set(REF.findall(s))-set(LABEL.findall(s)))
    require(all(k in other for k in missing),'Missing external labels '+str([k for k in missing if k not in other]))
    rows=['% BEGIN V171 COMPANION REFERENCES','\\makeatletter']
    for key in missing:
        num,page=other[key];rows.append('\\@namedef{r@'+key+'}{{'+prefix+'.'+num+'}{'+prefix+'.'+page+'}{}{}{}}')
    rows+=['\\makeatother','% END V171 COMPANION REFERENCES']
    return s.replace('\\begin{document}','\n'.join(rows)+'\n\\begin{document}',1)

def build(templates):
    for name in templates:
        for ext in ('.aux','.out','.toc'):(HERE/(name+ext)).unlink(missing_ok=True)
    for name in ('reconstruction','technical-supplement'):compile_one(name)
    stable=False
    for i in range(7):
        before={n:aux(n) for n in ('reconstruction','technical-supplement')}
        for n,o,prefix in [('reconstruction','technical-supplement','S'),('technical-supplement','reconstruction','I')]:
            (HERE/(n+'.tex')).write_text(embed(templates[n],before[o],prefix))
            compile_one(n)
        after={n:aux(n) for n in before}
        if before==after:stable=True;break
    require(stable,'External reference pagination unstable')
    compile_one('divisor-geometry',3);compile_one('geometry',3)
    outputs={};index={}
    for name in templates:
        text=(HERE/(name+'.log')).read_text(errors='replace')
        bad=[x for x in ('There were undefined references','There were multiply-defined labels','Overfull \\hbox','LaTeX Warning: Reference','LaTeX Warning: Citation') if x in text]
        require(not bad,'Layout or reference errors in '+name+': '+str(bad))
        info=subprocess.check_output(['pdfinfo',str(HERE/(name+'.pdf'))],text=True)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        outputs[name]={'pages':pages,'pdf_sha256':sha(HERE/(name+'.pdf')),'tex_sha256':sha(HERE/(name+'.tex')),'clean_references_and_no_overfull_hboxes':True}
        subprocess.run(['pdftotext','-layout',str(HERE/(name+'.pdf')),str(HERE/(name+'.txt'))],check=True)
        if name!='geometry':
            a=aux(name)
            for key in LABEL.findall(templates[name]):
                if key in a:index[key]={'paper':name,'number':a[key][0],'page':a[key][1]}
    ma=aux('geometry')
    for key,record in index.items():
        if key in ma:record.update(master_number=ma[key][0],master_page=ma[key][1])
    (HERE/'THEOREM_INDEX_V171.json').write_text(json.dumps(index,indent=2)+'\n')
    render=HERE/'render-audit';render.mkdir(exist_ok=True)
    selected={'reconstruction':{1},'technical-supplement':{1},'geometry':{1},'divisor-geometry':set(range(1,outputs['divisor-geometry']['pages']+1))}
    for name,pages in selected.items():
        for page in sorted(pages):
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1400','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return outputs,{n:sorted(v) for n,v in selected.items()}

def crosswalk():
    index=json.loads((HERE/'THEOREM_INDEX_V171.json').read_text());text='# Compiled locators for the v170 referee requests\n\n'
    for item in re.split(r'(?=^### \d+\.)',(HERE/'RESPONSE_TO_V170_REPORT.md').read_text(),flags=re.M)[1:]:
        text+=item.splitlines()[0]+'\n\n';keys=sorted(set(re.findall(r'(?:thm|cor|prop|lem|eq|sec|ex):[a-zA-Z0-9-]+',item)))
        entries=[]
        for key in keys:
            if key in index:
                x=index[key];entries.append(f'`{key}`: {x["paper"]}, {x["number"]}, p. {x["page"]}; archive p. {x.get("master_page","n/a")}')
        text+='; '.join(entries) if entries else 'See the documentary or CI evidence identified in the response.'
        text+='\n\n'
    (HERE/'REFEREE_CROSSWALK_V171.md').write_text(text)

def entry(r):
    text=f'# A2 revision 171 — referee entry\n\nBranch: `{BRANCH}`.\n\nControlling v170 report: `{REVIEW}`.\n\nComplete predecessor: `{PREDECESSOR}`.\n\nAuthored publication source: `{r["source_commit"]}`.\n\n'
    for n,title in [('reconstruction','Paper I — Finite failure schemes and the reconstruction of quadratic pencils'),('divisor-geometry','Paper II — '+TITLE)]:
        text+=f'## {title}\n\n{r["outputs"][n]["pages"]} pages. [PDF]({REL}/{n}.pdf) · [Standalone LaTeX]({REL}/{n}.tex).\n\n'
    text+='## Supplement and archive — not additional journal submissions\n\n'
    for n,title in [('technical-supplement','Complete technical supplement'),('geometry','Complete preservation master')]:
        text+=f'{title}: {r["outputs"][n]["pages"]} pages. [PDF]({REL}/{n}.pdf) · [LaTeX]({REL}/{n}.tex).\n\n'
    text+='''## New mathematical route

An actual-ideal conductor identity for arbitrary normal proper birational models
under finite flat smooth coefficient changes, in any dimension; trace-discriminant
normalization defects and associative conductor-divisor transitivity; a complete
self-contained marked chain proof; every divisorial conductor for tangent covers
b=u^r, c=u+v^s; the entire normalized square-tangency surface and scheme fibre in
all contact orders; and equal Hilbert limits with regular versus A1 normalization
germs. Diagonal local proofs are expanded, including an explicit unequal cover.
Classical trace duality and monomial integral closure are credited as inputs.

All 487 predecessor mathematical blocks and 706 master labels are retained.
Paper I's proofbody is unchanged; the complete predecessor Paper II mathematics
is typeset in the technical supplement. The new Paper II is independently readable.
The master is a repository archive, not a third submission.

'''
    for name,label in [('RESPONSE_TO_V170_REPORT.md','All 25 detailed responses'),('REFEREE_CROSSWALK_V171.md','Compiled theorem and page locators'),('THEOREM_DEPENDENCIES_V171.md','Proof dependencies'),('BUILD_RECEIPT_V171.json','Build and hash record'),('NONDELETION_V171.json','Exact proof preservation'),('EXACT_CHECKS_V171.json','Auxiliary exact checks'),('LITERATURE_AUDIT_V171.md','Primary-source comparison')]:
        text+=f'[{label}]({REL}/{name})\n\n'
    text+='''## Qualification and scope

Publication and exact-tip qualification are separate. After the generated outputs
are committed, the dedicated read-only submission workflow rebuilds and tests the
actual submitted tip in a temporary copy; it never self-publishes another commit.
Its check run and downloadable receipt bind the exact GITHUB_SHA. Do not infer
an administratively enforced branch-protection rule from a successful workflow.

The complete square-tangency classification is not the full B_a Hilbert fibre.
The general conductor identity does not classify all higher-corank or singular
pencils, nor does it normalize their embedded curves. No external independent
full Paper I audit or complete Ballico 1993 comparison has been obtained.
No finite check, hash or CI run is represented as a certificate of proof,
originality or journal acceptance. Previous branches and historical sources
remain unchanged.
'''
    (ROOT/'CURRENT_REVIEW_ENTRY.md').write_text(text)
    (ROOT/'A2_REVISION_V171_INDEX.md').write_text(text)
    (ROOT/'README.md').write_text('# Theta-Theory — A2 revision 171\n\n[Current referee entry](CURRENT_REVIEW_ENTRY.md) links the two publication papers, complete technical supplement, archived master, itemwise response, theorem locators and verification evidence.\n')
    (HERE/'CURRENT_REVIEW_ENTRY.md').write_text(text.replace(REL+'/',''))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
    templates,r=assemble();r['compiled']=False
    if args.build:
        checks=json.loads((HERE/'EXACT_CHECKS_V171.json').read_text())
        require(checks['all_checks_pass'],'Run exact checks first')
        for n,d in checks['source_sha256'].items():require(sha(HERE/n)==d,'Stale exact checks '+n)
        if os.environ.get('GITHUB_ACTIONS'):require(checks['inherited_v170_full_chain_rerun'],'Remote build requires inherited chain')
        r['outputs'],r['rendered_pages']=build(templates);r['compiled']=True
        r['inherited_v170_full_chain_rerun']=checks['inherited_v170_full_chain_rerun']
        r['external_references_stabilized']=True
        crosswalk();entry(r)
    r['authored_source_sha256']={p.name:sha(p) for p in HERE.iterdir() if p.name in PARTS or p.suffix=='.py'}
    r['supporting_document_sha256']={n:sha(HERE/n) for n in ('RESPONSE_TO_V170_REPORT.md','LITERATURE_AUDIT_V171.md','THEOREM_DEPENDENCIES_V171.md','CONTROLLING_REFEREE_REPORT_V170.md')}
    (HERE/'BUILD_RECEIPT_V171.json').write_text(json.dumps(r,indent=2)+'\n')
    for n,pin in PINS.items():require(sha(HERE.parent/'v170'/(n+'.tex'))==pin,'Predecessor modified '+n)
    print(json.dumps({'compiled':r['compiled'],'retained':r['predecessor_math_blocks'],'total_blocks':r['current_math_blocks'],'outputs':r.get('outputs')},indent=2))
if __name__=='__main__':main()
