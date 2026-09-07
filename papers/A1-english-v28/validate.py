#!/usr/bin/env python3
"""Replay inherited finite tests and check v24 preservation/builds, not proofs."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import argparse,hashlib,json,platform,subprocess,sys,time
from pathlib import Path
import build
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'validation'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(command,log,cwd=ROOT):
    start=time.monotonic()
    with log.open('w') as out:
        p=subprocess.run(command,cwd=cwd,stdout=out,stderr=subprocess.STDOUT,timeout=180)
    if p.returncode:raise RuntimeError(f'Failed: {command}; see {log}')
    return round(time.monotonic()-start,3)
def phase_checks():
    counts=Counter()
    def check(c,name):
        if not c:raise ValueError(name)
        counts[name]+=1
    for k in range(2,21):
        b1=F(6);b2=F(8*k-2)
        e=lambda b:(b/3,F(1,2)+b/4,F(4+2*k,9)+2*b/9)
        check(e(b1)[0]==e(b1)[1]==2,'first_crossover')
        check(e(b2)[1]==e(b2)[2]==2*k,'second_crossover')
        check(b2>b1,'separated_orders')
        for b,active in ((F(3),0),((b1+b2)/2,1),(b2+3,2)):
            check(e(b)[active]==min(e(b)),'three_dominant_regimes')
        for t in (F(1,16),F(1,64)):
            u=t/2;v=u+u**k
            check(u<=max(abs(u),abs(v))<=2*u,'rho_comparison')
            check(min(abs(u),abs(v-u),abs(v-2*u))==u**k,'tau_order')
    for b in (F(0),F(1),F(7,2),F(20)):
        six=b/3;eight=F(1,2)+b/4;seven=F(2,7)+2*b/7
        check(seven==F(3,7)*six+F(4,7)*eight,'seventh_branch_interpolation')
        check(seven>=min(six,eight),'seventh_branch_not_dominant')
    A=(0,1,3);future={a+b for a in A for b in A}
    check(len(future)-1==5 and min(len(A)-1,len(future)-1)==2,'acquired_dimension')
    t=(ROOT/'risk_criteria.tex').read_text()
    check(t.count(r'\inf_{F\in\mathcal F_M}\max_{1\le n<N}')==2,'causal_quantifier_order')
    check('conditioned on a selected' in t,'unconditional_law_named')
    return {'checks':sum(counts.values()),'groups':dict(counts),
            'scope':'Exact finite phase arithmetic/source regressions, not uniform analytic constants.'}
def mutation_checks():
    tests=[('main theorem weakening','text/main_classification.tex',b'integer $M\\ge1$',b'integer $M\\ge2$'),
      ('direct proof removal','main.tex',b'\\input{text/collision_direct}',b''),
      ('companion proof removal','companions.tex',b'\\input{sections/algebra_transfer_alternative}',b''),
      ('history mutation','history/v23-source/main.tex',b'\\begin{document}',b'\\begin{document}\nMUTATION'),
      ('unrecorded proof change','sections/classical.tex',b'Writing $T=I+U$',b'Writing $T=2I+U$')]
    result=[]
    for name,f,old,new in tests:
        p=ROOT/f;original=p.read_bytes()
        if old not in original:raise ValueError('Mutation anchor absent: '+name)
        try:
            p.write_bytes(original.replace(old,new,1))
            try:build.prepare()
            except (ValueError,RuntimeError) as exc:result.append({'mutation':name,'rejected':True,'exception':str(exc)})
            else:raise RuntimeError('Accepted mutation: '+name)
        finally:p.write_bytes(original)
    build.prepare();return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true',help='Also rerun older author suites; may be slow.');parser.add_argument('--resume',action='store_true',help='Reuse matching completed diagnostic receipts; rerun preservation tests and builds.');args=parser.parse_args()
    OUT.mkdir(exist_ok=True);receipt=OUT/'EXECUTION_REPORT.json';receipt.unlink(missing_ok=True)
    previous=json.loads((OUT/'PROGRESS.json').read_text()) if args.resume and (OUT/'PROGRESS.json').exists() else {}
    previous_suites={x['version']:x for x in previous.get('author_suites',[])}
    report={'version':24,'python':platform.python_version(),'review_basis':build.REVIEW,
            'history_identity':build.verify_history(),'validation_driver_sha256':digest(Path(__file__)),
            'build_driver_sha256':digest(ROOT/'build.py'),'author_suites':[]}
    H=ROOT/'history/v23-source'
    versions=(*range(10,16),17,18,19,20,21,22,23) if args.full else (22,23)
    report['suite_selection']='full' if args.full else 'focused v22-v23; older optional suites not certified by this run'
    for v in versions:
        script=H/(f'tests/test_v{v}.py' if v<18 else f'tests/verify_v{v}.py')
        result=OUT/f'V{v}_AUTHOR_RERUN.json'
        cached=previous_suites.get(v)
        reuse=bool(args.resume and cached and result.exists() and cached['source_sha256']==digest(script) and cached['receipt_sha256']==digest(result))
        seconds=cached['seconds'] if reuse else run([sys.executable,str(script),str(result)],OUT/f'author-v{v}.log',H)
        data=json.loads(result.read_text())
        if not (data.get('passed') is True or data.get('status')=='passed') or data.get('assertions',0)<=0:
            raise ValueError(f'Invalid v{v} receipt')
        report['author_suites'].append({'version':v,'assertions':data['assertions'],'passed':True,
            'seconds':seconds,'completed_receipt_reused':reuse,'source_sha256':digest(script),'receipt_sha256':digest(result)})
        (OUT/'PROGRESS.json').write_text(json.dumps(report,indent=2)+'\n')
        print('completed inherited suite',v,flush=True)
    report['inherited_author_assertions_total']=sum(x['assertions'] for x in report['author_suites'])
    for v in (22,23):
        result=OUT/f'V{v}_OPTIMIZED.json'
        if not (args.resume and result.exists() and result.read_bytes()==(OUT/f'V{v}_AUTHOR_RERUN.json').read_bytes()):
            run([sys.executable,'-O',str(H/f'tests/verify_v{v}.py'),str(result)],OUT/f'author-v{v}-optimized.log',H)
        if result.read_bytes()!=(OUT/f'V{v}_AUTHOR_RERUN.json').read_bytes():raise ValueError('Optimized author receipt differs')
    script=ROOT/'review-basis/independent_diagnostics.py'
    if digest(script)!='ff016f3e169fe6729d7408d17d7c68e70d71a93dc8c322c6e58023cf1c14191a':raise ValueError('Referee script mismatch')
    outputs=[]
    for flag,name in (([],'REFEREE_V23_RERUN.json'),(['-O'],'REFEREE_V23_OPTIMIZED.json')):
        target=OUT/name
        cached=json.loads(target.read_text()) if args.resume and target.exists() else {}
        if cached.get('script_sha256')!=digest(script) or cached.get('status')!='passed' or cached.get('total_checks')!=3878:
            run([sys.executable,*flag,str(script),str(target)],OUT/(name+'.log'))
        outputs.append(target)
    if outputs[0].read_bytes()!=outputs[1].read_bytes():raise ValueError('Optimized referee receipt differs')
    rr=json.loads(outputs[0].read_text())
    if (rr['status'],rr['total_checks'])!=('passed',3878):raise ValueError('Unexpected referee result')
    report['referee_v23_replay']={'checks':3878,'passed':True,'optimized_byte_identical':True,
        'script_sha256':digest(script),'resume_requested':args.resume,'scope':'Published referee script replayed by the revising assistant, not a new independent assessment.'}
    report['v24_phase_and_risk_checks']=phase_checks()
    report['preservation_mutations']=mutation_checks()
    report['build']=build.build()
    report['final_history_identity']=build.verify_history();report['passed']=True
    report['scope']='Executed finite regressions, source-preservation rejection tests and LaTeX builds. Not formal proof verification, a new independent audit, exhaustive priority search or journal acceptance.'
    receipt.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
