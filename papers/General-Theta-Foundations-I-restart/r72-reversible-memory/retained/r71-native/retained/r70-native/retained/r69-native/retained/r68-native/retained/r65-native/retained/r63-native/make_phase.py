"""Reproduce the exact comparator's phase data and its native LaTeX figure."""
from pathlib import Path
import math,json,argparse
import numpy as np
from scipy.optimize import brentq,minimize_scalar
ROOT=Path(__file__).resolve().parent
BREAKS=[6-2*math.sqrt(6),(16*math.sqrt(6)-24)/5,8*(math.sqrt(2)-1),32/5,36/5]
def optimum(b):
    t=BREAKS
    if b<=t[0]: return 1-b/2
    if b<=t[1]: return 2*b/(math.sqrt(b*b+12*b)+b)
    if b<=t[2]: return 1-b/8
    if b<=t[3]: return brentq(lambda s:128*s**4-b**3*(1-s),0,1,xtol=1e-14)
    if b<=t[4]: return b/8
    return 18*b/(math.sqrt(81*b*b+288*b)+9*b)
def objective(b,s):
    return max(4*s**3/b**2,s*s/(2*b))+max(2*(1-s)**2/b,(1-s)**1.5/math.sqrt(2*b))
def diagnostics():
    rows=[]
    for b in np.unique(np.concatenate([np.geomspace(1,100,180),BREAKS])):
        lo,hi=max(0,1-b/2),min(1,b/2)
        opt=minimize_scalar(lambda s:objective(b,s),bounds=(lo,hi),method='bounded',options={'xatol':1e-13}) if hi>lo else None
        exact=optimum(b); value=objective(b,exact)
        numeric=min([objective(b,lo),objective(b,hi)]+([opt.fun] if opt else []))
        if not lo-1e-12<=exact<=hi+1e-12 or abs(value-numeric)>2e-8:
            raise RuntimeError((b,exact,value,numeric))
        rows.append({'b':float(b),'s':exact,'objective':value,'independent_gap':value-numeric})
    return rows
if __name__=='__main__':
    rows=diagnostics()
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    out=ap.parse_args().out.resolve()
    if out==ROOT or ROOT in out.parents:raise ValueError('Write generated data outside immutable source')
    out.mkdir(parents=True,exist_ok=True)
    # Native LaTeX picture, without external plotting or font dependencies.
    x=lambda b:38+350*math.log(b)/math.log(30)
    y=lambda s:22+142*s
    lines=[r'\setlength{\unitlength}{1pt}',r'\begin{picture}(410,210)(0,-14)',r'\put(38,22){\line(1,0){350}}',r'\put(38,22){\line(0,1){145}}',r'\put(0,182){$s_*(b)$}']
    for s in [0,.5,1]:lines+=[f'\\put(34,{y(s):.3f}){{\\line(1,0){{4}}}}',f'\\put(8,{y(s)-3:.3f}){{\\makebox(23,8)[r]{{$ {s:g} $}}}}']
    for b in [1,2,5,10,30]:lines+=[f'\\put({x(b):.3f},18){{\\line(0,1){{4}}}}',f'\\put({x(b)-8:.3f},3){{\\makebox(16,9){{$ {b:g} $}}}}']
    lines.append(r'\put(174,-11){$b$ (logarithmic scale)}')
    for i,b in enumerate(BREAKS):
        lines.extend([r'\thinlines',f'\\put({x(b):.3f},22){{\\line(0,1){{142}}}}',f'\\put({x(b)-7:.3f},{170+8*(i%2):.3f}){{\\makebox(14,8){{$b_{i+1}$}}}}'])
    points=sorted(set(np.geomspace(1,30,65).tolist()+BREAKS))
    lines.append(r'\thicklines')
    for a,b in zip(points,points[1:]):
        xa,ya,xb,yb=x(a),y(optimum(a)),x(b),y(optimum(b))
        lines.append(f'\\qbezier({xa:.3f},{ya:.3f})({(xa+xb)/2:.3f},{(ya+yb)/2:.3f})({xb:.3f},{yb:.3f})')
    lines.append(r'\end{picture}')
    (out/'strata-phase.tex').write_text('\n'.join(lines)+'\n')
    (out/'strata-phase-data.json').write_text(json.dumps({'breakpoints':BREAKS,'data':rows},indent=2)+'\n')
    print('phase checks',len(rows),'maximum objective gap',max(abs(r['independent_gap']) for r in rows))
