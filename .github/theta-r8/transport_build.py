EDITS = {
'build.py': ('build.py', [
(1, 2, r'''"""Build the native R8 and the unchanged R6 companion; never modify source."""
'''),
(10, 10, r'''from supplement_build import cover_and_attach
'''),
(37, 38, r'''    with tempfile.TemporaryDirectory(prefix='theta-r8-receipts-') as tmp:
'''),
(46, 47, r'''        native_build.PAPER = 'General_Theta_Foundations_I_restart_r8.pdf'
'''),
(57, 58, r'''            output / 'General_Theta_Foundations_I_retained_technical_text.pdf')
'''),
(63, 64, r'''        result['component'] = 'General Theta Foundations I restart R8'
'''),
(66, 69, r'''        result['supplement'] = cover_and_attach(output/'General_Theta_Foundations_I_retained_technical_text.pdf', output/'General_Theta_Foundations_I_Supplement_S.pdf')
        result['companion_pdf'] = 'General_Theta_Foundations_I_Supplement_S.pdf'
        result['total_isolated_pdf_builds'] = 6
        result['technical_pdf_builds'] = 4
        result['cover_pdf_builds'] = 2
        result['limitations'] = ('Complete R8 native source and complete unchanged R6 companion only; '
'''),
]),
'native_build.py': ('native_build.py', [
(13, 14, r'''PAPER='General_Theta_Foundations_I_restart_r8.pdf'
'''),
(42, 43, r'''        with tempfile.TemporaryDirectory(prefix='theta-r8-clean-') as td:
'''),
(81, 82, r'''       'limitations':'Native r8 subtree build, not a repository-wide rebuild; finite regression does not prove theorems.'}
'''),
]),
'refresh_manifest.py': ('refresh_manifest.py', [
(11, 12, r'''    'scope': 'R8 native sources, excluding artifacts/evidence and this self-excluded manifest',
'''),
]),
'regression.py': ('regression.py', [
(1, 2, r'''"""Finite witnesses for cut comparison, companding, tuple size and Gaussian algebra.
The continuous-parameter arguments are in the manuscript, not in this suite.
"""
'''),
(6, 7, r''''''),
(8, 9, r''''''),
(12, 13, r'''counts=Counter()
def check(ok, group):
    if not ok: raise RuntimeError('regression failed: '+group)
    counts[group]+=1
'''),
(14, 14, r'''def quant(x,k):
    sign=1 if x>=0 else -1; x=abs(x)
    j=int(k*x/(1+x))
    return sign*F(j,k-j)
'''),
(15, 19, r'''def distortion(mu,kernel,z,labels):
    nc=max(labels)+1; nu=len(kernel[0]); value=F(0)
    for c in range(nc):
        for u in range(nu):
            mass=sum(mu[h]*kernel[h][u] for h in range(len(mu)) if labels[h]==c)
            if not mass: continue
            mean=sum(mu[h]*kernel[h][u]*z[h][u] for h in range(len(mu)) if labels[h]==c)/mass
            value+=sum(mu[h]*kernel[h][u]*(z[h][u]-mean)**2 for h in range(len(mu)) if labels[h]==c)
    return value
'''),
(20, 20, r'''def optimum(mu,kernel,z,M):
    return min(distortion(mu,kernel,z,labels) for labels in product(range(M),repeat=len(mu)))
'''),
(21, 149, r'''def mm(A,B): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A): return list(map(list,zip(*A)))
def plus(*args): return [[sum(a[i][j] for a in args) for j in range(len(args[0][0]))] for i in range(len(args[0]))]
def scale(a,A): return [[a*x for x in row] for row in A]
def eye(d): return [[F(i==j) for j in range(d)] for i in range(d)]
def outer(a,b): return [[x*y for y in b] for x in a]
def det(A):
    a=[row[:] for row in A]; result=F(1)
    for i in range(len(a)):
        piv=next((j for j in range(i,len(a)) if a[j][i]),None)
        if piv is None: return F(0)
        if piv!=i: a[i],a[piv]=a[piv],a[i];result=-result
        v=a[i][i];result*=v
        for j in range(i+1,len(a)):
            q=a[j][i]/v
            for k in range(i,len(a)): a[j][k]-=q*a[i][k]
    return result
'''),
(151, 165, r'''    for k in range(1,33):
        reps=set()
        for num in range(-180,181):
            x=F(num,7);q=quant(x,k);reps.add(q)
            check(abs(x-q)<=(1+abs(x))**2/k,'global_compander_point_bound')
            check(abs(q)<=abs(x),'compander_inwardness')
        check(len(reps)<=2*k-1,'compander_cardinality')
    for M in range(1,257):
        for d in range(1,9):
            m=1
            while (m+1)**d<=M: m+=1
            k=(m+1)//2
            check(2*k-1<=m,'per_coordinate_alphabet')
            for j in range(d+1): check(m**j<=M,'all_intermediate_tuple_counts')
            check(M<= (4*k)**d,'uniform_compander_budget_conversion')
    mu=[F(1,6),F(1,3),F(1,2)]; eta=[F(1,2),F(1,2)]
    for probabilities in product([F(1,4),F(1,2),F(3,4)],repeat=3):
        K=[[x,1-x] for x in probabilities]; independent=[eta]*3
        lo=min(2*x for row in K for x in row); hi=max(2*x for row in K for x in row)
        for z in [[[F(0),F(1)],[F(1,3),F(1,2)],[F(1),F(0)]],
                  [[F(1,4),F(3,4)],[F(1,2),F(2,3)],[F(3,4),F(1,4)]]]:
            for M in [1,2,3]:
                actual=optimum(mu,K,z,M); reference=optimum(mu,independent,z,M)
                check(lo*reference<=actual<=hi*reference,'finite_common_channel_sandwich')
                check(optimum([lo*x for x in mu],independent,z,M)==lo*reference,'submeasure_mass_scaling')
    for d in range(2,7):
        I=eye(d);a=[F(j+1,d) for j in range(d)];aa=outer(a,a);aa2=sum(x*x for x in a)
        for tau2,sigma2 in product([F(1,3),F(1),F(3)],repeat=2):
            c=1/(1+tau2);v0=tau2/(1+tau2);sv=sigma2+v0*aa2
            k=[v0*x/sv for x in a];D=plus(I,scale(-1,outer(k,a)))
            S=plus(scale(v0,I),scale(-v0*v0/sv,aa))
            precision=plus(scale(1/v0,I),scale(1/sigma2,aa))
            check(mm(precision,S)==I,'posterior_precision_inverse')
            check(det(D)==sigma2/sv,'continuation_full_rank')
            check(S==scale(v0,D),'conditional_covariance_algebra')
            Da=[row[0] for row in mm(D,[[x] for x in a])]
            C=plus(scale(c*c*(1+tau2),mm(D,tr(D))),scale(aa2+sigma2,outer(k,k)),
                   scale(c,outer(Da,k)),scale(c,outer(k,Da)))
            check(C==plus(I,scale(-1,S)),'actual_posterior_total_covariance')
            for n in range(1,d+1):
                check(det([row[:n] for row in S[:n]])>0,'positive_posterior_minors')
                check(det([row[:n] for row in C[:n]])>0,'positive_acquired_mean_minors')
    # These negative controls are finite analogues, not proofs of the continuum examples.
    check(F(1,2)*F(1,4)!=F(1,4),'negative:do_not_normalize_submass')
    check(8*3>8,'negative:stored_phase_multiplies_full_tuple')
    check(F(0)<F(1,8),'negative:defect_allowance_is_not_risk_floor')
    cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).with_name('regression_previous.py'))]
    run=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if run.returncode: raise RuntimeError(run.stdout)
    previous=json.loads(run.stdout);check(previous['status']=='PASS','retained_R7_suite')
    print(json.dumps({'status':'PASS','native_checks':sum(counts.values()),'groups':dict(sorted(counts.items())),
                     'retained_R7':previous,'scope':'finite exact-arithmetic witnesses; no continuum theorem certification'},sort_keys=True,indent=2))
'''),
(166, 169, r'''if __name__=='__main__': main()
'''),
]),
'regression_inherited.py': ('regression_inherited.py', [
]),
'regression_previous.py': ('regression.py', [
]),
'verify.py': ('verify.py', [
(1, 2, r'''"""Read-only source, reference, and dependency audit for the native r8 subtree."""
'''),
]),
}
TEXTS = {
'supplement_build.py': r'''#!/usr/bin/env python3
"""Attach the source-controlled submission cover to the unchanged technical PDF."""
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from pypdf import PdfReader, PdfWriter
from verify import ROOT, require, sha256, git_hash

def command(args, cwd=None, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    require(result.returncode == 0, 'supplement command failed: '+result.stdout[-10000:])
    return result.stdout

def cover_and_attach(raw_pdf, output_pdf):
    raw_pdf, output_pdf = Path(raw_pdf), Path(output_pdf)
    original = raw_pdf.read_bytes()
    retained = PdfReader(io.BytesIO(original))
    template = (ROOT/'supplement_cover.tex.in').read_bytes()
    env = os.environ.copy()
    env.update(SOURCE_DATE_EPOCH='1791331200', FORCE_SOURCE_DATE='1', TZ='UTC', LC_ALL='C.UTF-8')
    products=[]
    for _ in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-supplement-cover-') as tmp:
            p=Path(tmp); (p/'cover.tex').write_bytes(template)
            for _pass in range(3):
                command(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','cover.tex'],cwd=p,env=env)
            log=(p/'cover.log').read_text(errors='replace')
            for forbidden in ('Overfull \\hbox','Overfull \\vbox','There were undefined references'):
                require(forbidden not in log,'supplement cover: '+forbidden)
            cover=PdfReader(str(p/'cover.pdf')); require(len(cover.pages)==1,'cover must have one page')
            writer=PdfWriter()
            writer.append(cover, import_outline=False)
            writer.append(PdfReader(io.BytesIO(original)), import_outline=False)
            writer.add_metadata({'/Title':'Supplement S to General Theta Foundations I', '/Author':'Qian Qi'})
            data=io.BytesIO(); writer.write(data); data=data.getvalue()
            merged=PdfReader(io.BytesIO(data))
            require(len(merged.pages)==len(retained.pages)+1,'supplement page loss')
            for old,new in zip(retained.pages,list(merged.pages)[1:]):
                require(old.extract_text()==new.extract_text(),'technical page text changed during attachment')
            products.append(data)
    require(products[0]==products[1],'supplement attachment not byte reproducible')
    require(raw_pdf.read_bytes()==original,'raw technical PDF mutated')
    output_pdf.write_bytes(products[0])
    return {'status':'PASS', 'cover_source_sha256':sha256(template), 'cover_isolated_builds':2,
            'passes_per_cover':3, 'merged_byte_identical':True, 'raw_text_unchanged':True,
            'raw_pdf_sha256':sha256(original), 'pdf_sha256':sha256(products[0]),
            'pdf_git_blob_sha':git_hash('blob',products[0]), 'pdf_pages':len(retained.pages)+1,
            'formal_status':'Supplement S, integral part of this submission, not an external publication'}
''',
'supplement_cover.tex.in': r'''\documentclass[11pt]{amsart}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,microtype}
\usepackage[margin=1.08in]{geometry}
\pdfinfoomitdate=1
\pdftrailerid{}
\pdfsuppressptexinfo=15
\pagestyle{empty}
\begin{document}
\begin{center}
\vspace*{1.2in}
{\Large\scshape Supplement S}\par\bigskip
{\large General Theta Foundations I:\\[4pt]
Acquired Geometry and Causal Resource Transfer}\par\bigskip
Qian Qi\par\medskip
7 October 2026
\end{center}
\vspace{0.6in}
\noindent This supplement forms part of the same manuscript package and is supplied in full for joint review with the main article. It is not a separately published or accepted article.

\medskip\noindent The following complete technical text retains the proofs for prepared kernels and predictive realization, relation-preserving block transfer, acquisition and bounded stopping, sparse hidden-state filtering, nonreset singular dynamics, and fully typed causal experiment morphisms. Its theorem and section numbering is local to this supplement. References from the main article to ``Supplement S, Section~5,'' for example, refer to that local numbering.

\medskip\noindent The singular realization in the main article uses the complete proof in Section~5 below. The typed transcript construction used in the comparison theorem is given in Section~6 below. Neither dependence is on an unavailable external publication.

\vfill
\noindent\textit{Contents of the technical text.}
Prepared experiments; a raw-kernel block theorem; finite acquisition and stopping; sparse Gaussian filtering; nonreset singular acquisition; causal morphisms and resource accounts; comparison and scope.
\end{document}
''',
}
