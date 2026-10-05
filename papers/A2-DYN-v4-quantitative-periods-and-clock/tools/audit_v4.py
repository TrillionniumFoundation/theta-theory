#!/usr/bin/env python3
"""Source preservation and finite arithmetic, not continuum certification.

Requires build/excursion.json from the retained certificate script.
All failure checks remain active with python -O.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from pathlib import Path
import json
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
def blob(data):
    return sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def run():
    checks=0
    def need(condition,message):
        nonlocal checks
        checks+=1
        if not condition: raise ValueError(message)
    baseline=json.loads((ROOT/'PROOF_BASELINE.json').read_text())
    need(baseline['base_commit']=='55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191','base commit')
    closure=[]
    def visit(name):
        need(name not in closure,'recursive or duplicate TeX input')
        need(not Path(name).is_absolute() and '..' not in Path(name).parts,'unscoped input')
        path=ROOT/name
        need(path.is_file(),'missing source: '+name)
        closure.append(name)
        for sub in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
            visit(sub if sub.endswith('.tex') else sub+'.tex')
    visit('main.tex')
    need(set(closure)=={'main.tex','references.tex'}|{str(p.relative_to(ROOT)) for p in (ROOT/'core').glob('*.tex')},'incomplete closure')
    need(len(closure)==15,'closure count')
    text='\n'.join((ROOT/p).read_text() for p in closure)
    proofs=re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S)
    hashes=Counter(sha256(p.encode()).hexdigest() for p in proofs)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    need(len(labels)==len(set(labels)),'duplicate label')
    need(len(proofs)==37,'proof count')
    need(len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}',text))==37,'formal-result count')
    need(baseline['proof_count']==28 and baseline['label_count']==78,'baseline counts')
    for h,n in Counter(baseline['proof_hashes']).items():
        need(hashes[h]>=n,'old proof changed: '+h)
    need(set(baseline['labels'])<=set(labels),'old label missing')
    unchanged=[]
    for name,row in baseline['files'].items():
        need(name in closure,'inactive old source')
        if row['unchanged_required']:
            data=(ROOT/name).read_bytes()
            need(blob(data)==row['git_blob'] and sha256(data).hexdigest()==row['sha256'],'changed old source: '+name)
            unchanged.append(name)
    for label in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        need(label in labels,'undefined reference: '+label)
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text):
        for key in group.split(','): need(key.strip() in bib,'undefined citation')
    # Constants in the nonlinear action proof, evaluated as exact rationals.
    need(F(173,100)**2<3<F(174,100)**2,'sqrt3')
    need(F(9,20)**2-F(1,20)**2>F(11,25)**2,'x lower')
    need(F(173,200)-F(47,100)==F(79,200),'end horizontal lower')
    need(F(174,200)-F(11,25)==F(43,100),'end horizontal upper')
    need(F(43,100)**2+F(1,20)**2<F(11,25)**2,'end length upper')
    need(F(86,100)**2+F(1,20)**2<F(9,10)**2,'interior length upper')
    umax=F(47,100)**2/F(11,25)**3
    need(umax==F(55225,21296) and umax<3,'u curvature')
    need(F(79,88)*F(100,47)>F(3,2),'end lower curvature')
    need(F(79,90)*F(100,47)>F(3,2),'interior lower curvature')
    need((1+F(5,44)**2)/F(79,100)+umax<4,'interior diagonal')
    need((1+F(5,44)**2)/F(79,200)+umax<6,'end diagonal')
    need(F(79,100)-F(1,20)*F(5,44)>F(78,100),'mixed numerator lower')
    need(F(86,100)+F(1,20)*F(5,44)<F(87,100),'mixed numerator upper')
    need(F(78,100)**2/F(9,10)**3>F(1,2),'mixed derivative lower')
    need(F(87,100)**2/F(79,100)**3<2,'mixed derivative upper')
    need(F(3,100)/F(11,25)==F(3,44),'gradient lower')
    need(F(1,20)/F(79,200)<F(1,7),'gradient upper')
    need(F(1,21)**2/F(79,100)==F(100,34839)<F(1,300),'excess upper')
    need(2*F(3,440)**2/F(47,100)==F(9,45496)>F(1,10000),'excess lower')
    need(F(1,300)/(1-F(49,100))==F(1,153),'excess tail')
    need(15000*400**2==2400000000,'phase coefficient')
    cert=json.loads((ROOT/'build/excursion.json').read_text())
    need(cert['status']=='passed','finite certificate')
    rows={}
    for row in cert['samples']:
        e=row['excess_enclosure'];scale=10**e['denominator_power_10']
        rows[row['R'],row['m']]=(F(int(e['lower_numerator']),scale),F(int(e['upper_numerator']),scale))
    pairs=0
    for (radius,m),(lo,hi) in rows.items():
        if (radius,m+1) in rows:
            nlo,nhi=rows[radius,m+1]
            need(nlo-hi>=F(1,10000)*F(1,400)**m,'finite increment lower')
            need(nhi-lo<=F(1,300)*F(49,100)**(m-1),'finite increment upper')
            pairs+=1
    need(len(rows)==18 and pairs==15,'finite sample counts')
    for m in range(1,33):
        need((2*(m+1)+1)-(2*m+1)-2==0,'physical phase cancellation')
        need((m+1)-m-1==0,'induced phase cancellation')
        need(2*(m+1)-2*m-2==0,'base-length phase cancellation')
        need((m+1)+m+1==2*(m+1),'telescope budget')
    return {'schema':'a2-dyn-v4-source-and-finite-audit-1','status':'passed','checks':checks,
      'base_commit':baseline['base_commit'],'active_proofs':len(proofs),'active_labels':len(labels),
      'preserved_v3_proofs':28,'preserved_v3_labels':78,'new_proofs':9,
      'unchanged_core_files':unchanged,'finite_excursion_samples':len(rows),'finite_increment_pairs':pairs,
      'source_files':{p:{'git_blob':blob((ROOT/p).read_bytes()),'sha256':sha256((ROOT/p).read_bytes()).hexdigest()} for p in sorted(closure)},
      'scope':'Source preservation and finite rational arithmetic only; analytical proofs require mathematical review.',
      'full_billiard_LLT_verified':False,'continuum_proof_certificate':False,'independent_human_review':False}
if __name__=='__main__':
    try: print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (ValueError,KeyError,OSError,TypeError) as exc:
        print(json.dumps({'status':'failed','error':str(exc)},sort_keys=True));sys.exit(1)
