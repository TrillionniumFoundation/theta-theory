#!/usr/bin/env python3
"""Independent finite controls for the source-pinned A2 v38 review.

Run: python -B diagnostics.py; python -B -O diagnostics.py.
No native TeX/PDF build is performed. Finite controls do not prove theorems.
The local flight graphs below are not asserted to realize a periodic table.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
from fractions import Fraction as F
from pathlib import Path
import tempfile
import numpy as np

ROOT = Path(__file__).resolve().parent
SUBMISSION = '7b506becac7fc51dc1ea4f5ab407389d1208b07a'
FIXTURE_BLOB = 'd944aac5604f123795f5c744c2042176c353b981'
FIXTURE_SHA256 = '495061bf4962dd07f2e7b551a1488c9c9e09769a8e7ea4cda353f06bc8a47739'


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def provenance() -> dict:
    path = ROOT / 'fixtures/source_provenance.py'
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, 'Fixture SHA-256 mismatch')
    need(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
         == FIXTURE_BLOB, 'Fixture Git blob mismatch')
    spec = importlib.util.spec_from_file_location('reviewed_provenance', path)
    need(spec is not None and spec.loader is not None, 'Cannot load fixture')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cases = {}

    def run_case(name: str, change, accept: bool, marker: str = '') -> None:
        with tempfile.TemporaryDirectory(prefix='a2-v38-referee-') as temp:
            base = Path(temp)
            work = base / 'work'
            work.mkdir()
            (work / 'main.tex').write_text('\\input{body}\n')
            (work / 'body.tex').write_text('Native source body.\n')
            files = {}
            for p in sorted(work.iterdir()):
                b = p.read_bytes()
                files[p.name] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
                                 'git_blob': mod.blob_id(b)}
            lines = ['PWD ' + str(work), 'INPUT main.tex', 'INPUT body.tex']
            roots = []
            imported = {}
            change(base, work, files, lines, roots, imported)
            if lines is not None and '__ABSENT__' not in lines:
                (work / 'main.fls').write_text('\n'.join(lines) + ('\n' if lines else ''))
            try:
                got = mod.recorder_inputs('main', work, files,
                                          {'main.tex', 'body.tex'}, roots, imported)
            except Exception as exc:
                need(not accept, name + ': unexpectedly rejected: ' + str(exc))
                need(marker in str(exc), name + ': wrong rejection reason: ' + str(exc))
                cases[name] = 'rejected_as_required'
            else:
                need(accept, name + ': unexpectedly accepted')
                need(got['source_inputs']['main.tex']['git_blob'] == files['main.tex']['git_blob'],
                     name + ': wrong accepted native identity')
                cases[name] = 'accepted_control'

    noop = lambda *args: None
    run_case('matching_actual_bytes', noop, True)
    run_case('absent_recorder', lambda b,w,f,l,r,i: l.append('__ABSENT__'), False, 'Missing or empty')
    run_case('empty_recorder', lambda b,w,f,l,r,i: l.clear(), False, 'Missing or empty')
    run_case('missing_native_entry', lambda b,w,f,l,r,i: l.remove('INPUT main.tex'), False, 'Native entry')
    run_case('missing_recursive_input', lambda b,w,f,l,r,i: l.remove('INPUT body.tex'), False, 'Recursive native')
    run_case('wrong_working_directory', lambda b,w,f,l,r,i: l.__setitem__(0, 'PWD ' + str(b)),
             False, 'working directory')
    run_case('absent_working_directory', lambda b,w,f,l,r,i: l.pop(0), False, 'working directory')
    run_case('divergent_compilation_bytes', lambda b,w,f,l,r,i: (w/'body.tex').write_text('Mutated source body!\n'),
             False, 'Snapshot bytes differ')
    run_case('missing_snapshot_file', lambda b,w,f,l,r,i: (w/'body.tex').unlink(), False, 'Missing or symlinked')

    def unexplained(b,w,f,l,r,i):
        (w/'extra.tex').write_text('Unmanifested.\n')
        l.append('INPUT extra.tex')
    run_case('unexplained_local_input', unexplained, False, 'Unexplained local')

    def symlink(b,w,f,l,r,i):
        p=w/'body.tex'; data=p.read_bytes(); p.unlink(); (b/'outside.tex').write_bytes(data)
        p.symlink_to(b/'outside.tex')
    run_case('snapshot_symlink', symlink, False, 'Missing or symlinked')

    def external(b,w,f,l,r,i,approved):
        ext=b/'tex-install'; ext.mkdir(); p=ext/'package.sty'; p.write_text('Package.\n')
        l.append('INPUT '+str(p))
        if approved: r.append(ext)
    run_case('approved_external_package', lambda *a: external(*a, True), True)
    run_case('unapproved_external_input', lambda *a: external(*a, False), False, 'outside declared')

    def imported_aux(b,w,f,l,r,i,mode):
        p=w/'two_collision.aux'; p.write_text('Verified companion auxiliary.\n')
        i[p.name]={'bytes':p.stat().st_size, 'sha256':mod.sha256(p), 'producer_entry':'two_collision.tex'}
        if mode!='unrecorded': l.append('INPUT '+p.name)
        if mode=='mutated': p.write_text('Changed companion auxiliary.\n')
        if mode=='missing': p.unlink()
    run_case('verified_companion_auxiliary', lambda *a: imported_aux(*a, 'valid'), True)
    run_case('mutated_companion_auxiliary', lambda *a: imported_aux(*a, 'mutated'), False, 'differs from producer')
    run_case('missing_companion_auxiliary', lambda *a: imported_aux(*a, 'missing'), False, 'Missing or symlinked')
    run_case('unrecorded_companion_auxiliary', lambda *a: imported_aux(*a, 'unrecorded'), False, 'absent from recorder')
    run_case('source_generated_overlap', lambda b,w,f,l,r,i: i.update({'body.tex': f['body.tex']}),
             False, 'overlap')

    def own_aux(b,w,f,l,r,i,output):
        (w/'main.aux').write_text('Generated current auxiliary.\n'); l.append('INPUT main.aux')
        if output: l.append('OUTPUT main.aux')
    run_case('current_auxiliary_with_output', lambda *a: own_aux(*a, True), True)
    run_case('current_auxiliary_without_output', lambda *a: own_aux(*a, False), False, 'Unexplained local')
    run_case('duplicate_input_lines', lambda b,w,f,l,r,i: l.append('INPUT main.tex'), True)
    with tempfile.TemporaryDirectory() as temp:
        d=Path(temp)
        (d/'main.tex').write_text('% \\input{ignored}\n\\input{body}\n')
        (d/'body.tex').write_text('Body.\n')
        need(mod.graph(d, 'main.tex') == {'main.tex','body.tex'}, 'Static graph comment test')
        cases['recursive_graph_ignores_comments']='accepted_control'
        (d/'main.tex').write_text('\\input{\\dynamic}\n')
        try: mod.graph(d,'main.tex')
        except RuntimeError as exc: need('dynamic' in str(exc), 'Wrong dynamic-input failure')
        else: raise RuntimeError('Dynamic input unexpectedly accepted')
        cases['recursive_graph_rejects_dynamic']='rejected_as_required'
    return {'fixture_blob': FIXTURE_BLOB, 'fixture_sha256': FIXTURE_SHA256,
            'checks': len(cases), 'cases': cases,
            'scope': 'Exact verifier module; real temporary files; no TeX or full-CLI execution'}


def jacobi() -> dict:
    max_green = max_schur = max_twist = 0.0
    count=0
    for g,k0,k1 in [(0.7,0.8,1.3),(1.0,2.1,0.6),(0.4,0.5,0.9)]:
        c=np.array([1+g*k0,1+g*k1]); cc=math.sqrt(float(c.prod())); gam=math.acosh(cc)
        for j in [1,2,3,4,7,12,21]:
            H=np.zeros((j+1,j+1))
            for i in range(j):
                H[i,i]+=c[i%2]/g; H[i+1,i+1]+=c[(i+1)%2]/g
                H[i,i+1]=H[i+1,i]=-1/g
            ends=[0,j]; inner=list(range(1,j)); eff=H[np.ix_(ends,ends)]
            if inner:
                A=H[np.ix_(inner,inner)]; G=np.empty_like(A)
                for ii in inner:
                    for kk in inner:
                        l=min(ii,kk); h=max(ii,kk)
                        sig=math.sqrt(float(c[1-ii%2]*c[1-kk%2]))
                        G[ii-1,kk-1]=(g*sig/cc*math.sinh(l*gam)*math.sinh((j-h)*gam)
                                      /(math.sinh(gam)*math.sinh(j*gam)))
                max_green=max(max_green,float(np.max(np.abs(A@G-np.eye(j-1)))))
                E=H[np.ix_(ends,inner)]; eff=eff-E@np.linalg.solve(A,E.T)
                logtw=-j*math.log(g)-np.linalg.slogdet(A)[1]
            else: logtw=-math.log(g)
            D=np.diag([1/math.sqrt(float(c[1])),1/math.sqrt(float(c[1-j%2]))])
            mid=np.array([[1/math.tanh(j*gam),-1/math.sinh(j*gam)],
                          [-1/math.sinh(j*gam),1/math.tanh(j*gam)]])
            formula=cc*math.sinh(gam)/g*D@mid@D
            max_schur=max(max_schur,float(np.max(np.abs(eff-formula))))
            max_twist=max(max_twist,abs(math.exp(logtw)/(-formula[0,1])-1))
            count+=1
    need(max(max_green,max_schur,max_twist)<2e-12, 'Jacobi identity failed')
    return {'cases':count,'max_green_residual':max_green,'max_schur_error':max_schur,
            'max_relative_twist_error':max_twist}


def flight_edges(y: np.ndarray, g: float, kappas, thirds, fourths):
    idx=np.arange(len(y))%2; ka=np.asarray(kappas)[idx]; th=np.asarray(thirds)[idx]; fo=np.asarray(fourths)[idx]
    psi=ka*y*y/2+th*y**3/6+fo*y**4/24
    dp=ka*y+th*y*y/2+fo*y**3/6; dd=ka+th*y+fo*y*y/2
    h=g+psi[:-1]+psi[1:]; z=y[1:]-y[:-1]; length=np.hypot(h,z)
    va=h*dp[:-1]-z; vb=h*dp[1:]+z
    da=va/length; db=vb/length
    aa=(dp[:-1]**2+h*dd[:-1]+1)/length-va**2/length**3
    bb=(dp[1:]**2+h*dd[1:]+1)/length-vb**2/length**3
    ab=(dp[:-1]*dp[1:]-1)/length-va*vb/length**3
    return length,da,db,aa,bb,ab


def stationary(j,u,v,g,kappas,thirds,fourths):
    c=1+g*np.asarray(kappas); gam=math.acosh(math.sqrt(float(c.prod())))
    sig=np.sqrt(c[1-np.arange(j+1)%2]); t=np.arange(j+1)
    y=sig*(np.sinh((j-t)*gam)/math.sinh(j*gam)*u/sig[0]
           +np.sinh(t*gam)/math.sinh(j*gam)*v/sig[-1])
    last=0.0
    for it in range(20):
        lengths,da,db,aa,bb,ab=flight_edges(y,g,kappas,thirds,fourths)
        grad=db[:-1]+da[1:]; diag=bb[:-1]+aa[1:]
        A=np.diag(diag)+np.diag(ab[1:-1],1)+np.diag(ab[1:-1],-1)
        last=float(np.max(np.abs(grad)))
        if last<2e-15: break
        y[1:-1]-=np.linalg.solve(A,grad)
    need(last<2e-13,'Stationary residual too large')
    need(np.all(ab<0) and np.linalg.eigvalsh(A)[0]>0,'Local twist or Hessian failed')
    sign,ld=np.linalg.slogdet(A); need(sign>0,'Determinant not positive')
    q=math.sqrt(float(c[0]/c[1-j%2]))*math.sinh(gam)/g
    reference=q/math.sinh(j*gam)
    logb=float(np.sum(np.log(-ab))-ld-math.log(reference))
    return y,last,logb


def nonlinear() -> dict:
    g=0.7; ka=[0.8,1.3]; th=[0.35,-0.27]; fo=[0.6,0.9]
    residuals=[]; comparisons=[]
    for b,u,v in [(0,0.045,-0.03),(1,-0.04,0.025)]:
        kb=ka[b:]+ka[:b]; tb=th[b:]+th[:b]; fb=fo[b:]+fo[:b]
        left,rl,bl=stationary(64,u,0,g,kb,tb,fb)
        right,rr,br=stationary(64,v,0,g,kb,tb,fb)
        residuals.extend([rl,rr])
        errors=[]
        for j in [8,16,24]:
            y,r,both=stationary(j,u,v,g,kb,tb,fb); residuals.append(r)
            errors.append(abs(both-bl-br))
        need(errors[-1]<1e-9 and errors[1]<errors[0]/100,'Finite log-amplitude factorization failed')
        # Finite envelope derivative under a graph cubic-jet variation.
        lengths,*_=flight_edges(left,g,kb,tb,fb)
        idx=np.arange(65)%2; psi=np.asarray(kb)[idx]*left**2/2+np.asarray(tb)[idx]*left**3/6+np.asarray(fb)[idx]*left**4/24
        heights=g+psi[:-1]+psi[1:]
        node=left**3/6*(idx==0)
        envelope=float(np.sum(heights/lengths*(node[:-1]+node[1:])))
        step=1e-3; actions=[]
        for s in [-step,step]:
            changed=tb.copy(); changed[0]+=s
            yy,r,_=stationary(64,u,0,g,kb,changed,fb); residuals.append(r)
            # Stable excess length avoids subtracting g from nearly equal floats.
            ix=np.arange(65)%2
            pp=np.asarray(kb)[ix]*yy**2/2+np.asarray(changed)[ix]*yy**3/6+np.asarray(fb)[ix]*yy**4/24
            hh=g+pp[:-1]+pp[1:]; zz=yy[1:]-yy[:-1]
            actions.append(float(np.sum(pp[:-1]+pp[1:]+zz**2/(np.hypot(hh,zz)+hh))))
        fd=(actions[1]-actions[0])/(2*step)
        need(abs(fd-envelope)<1e-10,'Finite cubic envelope test failed')
        comparisons.append({'starting_type':b,'flight_counts':[8,16,24],
                            'log_amplitude_errors_against_64_flight_halflines':errors,
                            'finite_cubic_envelope_absolute_error':abs(fd-envelope)})
    return {'max_stationary_residual':max(residuals),'comparisons':comparisons,
            'scope':'Finite local asymmetric graph models, not a global periodic realization'}


def density_and_jets() -> dict:
    checks=0
    for x in range(-5,6):
        for y in range(-5,6):
            u=F(x,20); v=F(y,20); d=F(1)
            S=lambda z:z*z+z**3/F(5)+z**4/F(10)
            B=lambda z:1+z/F(7)+z*z/F(9)
            f=lambda a,b:B(a)*B(b)*(d-S(a)-S(b))/F(7)
            ratio=f(u,v)*f(0,0)/(f(u,0)*f(0,v))
            need(1-ratio==S(u)/(d-S(u))*S(v)/(d-S(v)), 'Exact density identity failed')
            checks+=1
    errors=[]
    for gam,r in [(0.3,1.2),(0.9,0.7),(1.4,1.6)]:
        for n in [3,4,7,12]:
            z=math.exp(-n*gam); own=(1+z*z)/(1-z*z); cross=2*z/(1-z*z)
            M=np.array([[own,r**n*cross],[r**(-n)*cross,own]])
            errors.append(abs(float(np.linalg.det(M))-1))
    need(max(errors)<2e-13,'Jet block determinant failed')
    return {'exact_signed_density_pairs':checks,'jet_blocks':len(errors),'max_jet_det_error':max(errors)}


def poisson_corner() -> dict:
    # Non-billiard radial control: w=1-|x|^2, rho=2/pi, ceiling w-a/k.
    # Normalize successful density by Z=(1-a/k)^2; use y=k(w-r).
    R=3.0; a=0.7; rows=[]
    for k in [50,100,200,400]:
        Z=(1-a/k)**2
        # Endpoint radial coordinate w has area element pi dw on the disk.
        # Lost layer triangle from r>0: 2*integral_a^R y/k dy / Z.
        corner_scaled=(R*R-a*a)/(k*Z)
        target_mass=2*(R-a)
        layer_scaled=(2*(R-a)-(R*R-a*a)/k)/Z
        upper=corner_scaled+abs(1/Z-1)*target_mass
        need(abs(layer_scaled-target_mass)<=upper+1e-14,'Layer TV budget failed')
        rows.append({'k':k,'scaled_corner_mass':corner_scaled,'layer_intensity_mass_error':abs(layer_scaled-target_mass),
                     'TV_mass_upper_bound':upper})
    need(rows[-1]['TV_mass_upper_bound']<rows[0]['TV_mass_upper_bound']/7,'Corner budget not decaying')
    return {'scope':'Normalized radial control, not a billiard-realizability assertion','rows':rows}


def main() -> None:
    result={'reviewed_submission':SUBMISSION,'status':'passed',
            'scope':'Independent finite controls; no TeX/PDF build or universal correctness certificate',
            'provenance':provenance(),'quadratic_jacobi':jacobi(),'nonlinear_local_flights':nonlinear(),
            'density_and_jet_blocks':density_and_jets(),'poisson_layer_corner':poisson_corner()}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
