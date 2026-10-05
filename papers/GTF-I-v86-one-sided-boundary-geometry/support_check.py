#!/usr/bin/env python3
"""Exact finite regressions for support geometry and finite-angle construction.

Universal continuum statements are proved in TeX, not established by this
suite. The logical BB84 example is a symbolic channel calculation, not a
physical device experiment or a synthesis of the general recovery.
"""
import copy,json
from pathlib import Path
import sympy as s
from matrix_metric import require,matrix_to_json
from covariance_metric import covariance,system,inner
from support_geometry import support_data,transported_energy,certify,verify,INPUT

checks=0;negative=0

def check(ok,msg):
    global checks
    require(bool(ok),msg);checks+=1

def reject(fn):
    global negative
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError):negative+=1;return
    raise RuntimeError('invalid case accepted')

I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
bb=[(I+v)/4 for v in [Z,-Z,X,-X]]
pauli=[(I+v)/6 for v in [X,-X,Y,-Y,Z,-Z]]
models=[('pvm',[(I+Z)/2,(I-Z)/2],2),('bb84',bb,3),('pauli6',pauli,4),
        ('noisy_bb84',[3*e/4+I/16 for e in bb],4),
        ('zero_effect',[I,s.zeros(2)],4),('split_projective',[(I+Z)/4,(I+Z)/4,(I-Z)/2],2),
        ('scalar',[s.Matrix([[s.Rational(1,3)]]),s.Matrix([[s.Rational(2,3)]]),s.zeros(1)],1)]
summary={}
for name,e,wdim in models:
 d=e[0].rows;gens=[s.eye(d)] if d==1 else [I,X,Y,Z]
 basis,gram,l=system(e)
 for g in gens:
  data=support_data(e,g);check(len(data['basis'])==wdim,name+' span dimension')
  check(data['kernel_dimension']==len(l.nullspace()),name+' kernel dimension')
  h=[s.I*(g*x-x*g) for x in e];rhs=s.Matrix([inner(v,h) for v in basis])
  check((l.row_join(rhs).rank()==l.rank())==data['in_span'],name+' tangent range')
  a=data['complement'];p=data['projections'];zz=s.zeros(d)
  xx=[s.I*(q*a-a*q) for q in p];mean=sum(xx,zz)/len(e);kt=[v-mean for v in xx]
  check(all(v==zz for v in covariance(e,kt)),name+' support kernel formula')
  check(s.simplify(inner(h,kt)+2*s.trace(g*a))==0,name+' exact commutator pairing')
  check(all(x*a*x==zz for x in p),name+' support complement')
  for j in range(len(e)):
   q=s.eye(d)-p[j];zt=[zz.copy() for _ in e];zt[j]=q
   zmean=sum(zt,zz)/len(e);zt=[v-zmean for v in zt]
   check(all(v==zz for v in covariance(e,zt)),name+' missing-support kernel')
  summary[name]= {'support_span_dimension':wdim,'kernel_dimension':data['kernel_dimension']}

check(support_data(bb,Y)['regime']=='linear','BB84 Y orbit')
check(support_data(bb,X)['regime']=='square_root','BB84 X orbit')
check(support_data(pauli,Y)['regime']=='square_root','IC rank-one orbit')
check(support_data([I,s.zeros(2)],Y)['regime']=='stationary','deterministic measurement')
# Coarse-graining incompatible BB84 supports gives a positive definite effect.
coarse=[bb[0]+bb[2],bb[1]+bb[3]]
check(support_data(coarse,Y)['regime']=='square_root','processing support inclusion')

# Real rational unitary changes preserve span membership and rank formula.
U=s.Matrix([[s.Rational(3,5),s.Rational(4,5)],[-s.Rational(4,5),s.Rational(3,5)]])
data=support_data([U*e*U.adjoint() for e in bb],U*Y*U.adjoint())
check(data['regime']=='linear' and len(data['basis'])==3,'rational unitary invariance')
check(support_data(list(reversed(bb)),Y)['kernel_dimension']==5,'label invariance')

# Processing-covariant ridge: a reversible split of the first label.
e=[(I+Z/3)/2,(I-Z/3)/2];h=[X/10,-X/10];w=[s.Rational(1,2)]*2
T=s.Matrix([[s.Rational(1,3),0],[s.Rational(2,3),0],[0,1]])
def mapped(t,tuple_):return [sum((t[a,j]*tuple_[j] for j in range(t.cols)),s.zeros(2)) for a in range(t.rows)]
for tau in [s.Rational(1,7),s.Rational(1),s.Rational(5,2)]:
 value=transported_energy(e,w,h,tau)
 split=transported_energy(mapped(T,e),list(T*s.Matrix(w)),mapped(T,h),tau)
 check(split==value,'transported ridge reversible split equality')
 # Zero output row is retained in the extended-energy computation.
 TZ=s.Matrix([[1,0],[0,1],[0,0]])
 check(transported_energy(mapped(TZ,e),list(TZ*s.Matrix(w)),mapped(TZ,h),tau)==value,
       'zero output-row energy')
TC=s.Matrix([[s.Rational(3,4),s.Rational(1,4)],[s.Rational(1,4),s.Rational(3,4)]])
check(transported_energy(mapped(TC,e),list(TC*s.Matrix(w)),mapped(TC,h),1)<=transported_energy(e,w,h,1),
      'transported ridge noisy coarse-graining')
check(transported_energy([I,s.zeros(2)],[1,0],[X,-X],1) is None,'infinite off-range energy')

# Exact logical-qubit channel for a nonprojective measurement (BB84).
# The columns are input |+y>,|-y> tensored with orthogonal external flags.
vp=s.Matrix([1,s.I])/s.sqrt(2);vm=s.Matrix([1,-s.I])/s.sqrt(2)
f0=s.Matrix([1,0]);f1=s.Matrix([0,1])
J=s.Matrix.hstack(s.kronecker_product(vp,f0),s.kronecker_product(vm,f1))
check(s.simplify(J.adjoint()*J)==I,'code normalization')
GL=s.simplify(J.adjoint()*s.kronecker_product(Y,I)*J)
check(GL==Z,'logical generator and gap')
# Rank-one measurement vectors including the sqrt(1/2) effect weight.
rows=[s.Matrix([[1,0]])/s.sqrt(2),s.Matrix([[0,1]])/s.sqrt(2),
      s.Matrix([[1,1]])/2,s.Matrix([[1,-1]])/2]
logical=[]
for j,row in enumerate(rows):
 block=s.simplify(s.kronecker_product(row,I)*J)
 check(s.simplify(block.adjoint()*block)==I/4,'equal syndrome weights')
 recovery=s.simplify(2*block.adjoint())
 check(s.simplify(recovery.adjoint()*recovery)==I,'conditional reference recovery')
 logical.append((row,recovery))
# Use rational unitary U=(3I-4iY)/5, avoiding numerical phases.
Utheta=(3*I-4*s.I*Y)/5;Ulogical=(3*I-4*s.I*Z)/5
for row,recovery in logical:
 actual=s.simplify(recovery*s.kronecker_product(row*Utheta,I)*J)
 check(actual==Ulogical/2,'exact corrected nonzero-angle channel')
# Knill--Laflamme checks for a higher-rank noise example are ordinary kernel
# identities above; no arbitrary code synthesis is represented as executed.
for a in [s.Rational(1,10),s.Rational(1,100),s.Rational(1,1000)]:
 for n in [1,2,7,100]:
  gap=s.Rational(2);m=min(n,int(1/(a*gap)));x=m*a*gap
  check(x<=1 and x>=min(1,n*a*gap)/2,'finite-angle flooring range')

raw={'schema':INPUT,'dimension':2,'outcomes':4,'effects':[matrix_to_json(v) for v in bb],
     'generator':matrix_to_json(Y)}
cert=certify(raw);check(verify(raw,cert)['status']=='success','certificate roundtrip')
(R:=Path(__file__).resolve().parent)
# The example file is independently parsed rather than regenerated at run time.
check(certify(json.loads((R/'examples/support-bb84.json').read_text()))==cert,'native example identity')
for field,value in [('finite_angle_regime','square_root'),('covariance_kernel_dimension',0),
 ('support_span_dimension',4),('generator_in_support_span',True),('recovery_synthesized',True),
 ('physical_protocol_executed',True),('input_sha256','0'*64),('theorem','other')]:
 bad=copy.deepcopy(cert);bad[field]=value;reject(lambda b=bad:verify(raw,b))
bad=copy.deepcopy(cert);bad['unexpected']=1;reject(lambda:verify(raw,bad))
bad=copy.deepcopy(raw);bad['outcomes']=3;reject(lambda:certify(bad))
bad=copy.deepcopy(raw);bad['dimension']=True;reject(lambda:certify(bad))
bad=copy.deepcopy(raw);bad['schema']='wrong';reject(lambda:certify(bad))
reject(lambda:certify(raw,2))
bad=copy.deepcopy(raw);bad['effects'][0]=matrix_to_json(-I);reject(lambda:certify(bad))
bad=copy.deepcopy(raw);bad['generator']=matrix_to_json(s.Matrix([[0,1],[0,0]]));reject(lambda:certify(bad))
reject(lambda:transported_energy(e,[1,1],h,1))
reject(lambda:transported_energy(e,w,h,0))
reject(lambda:transported_energy(e,w,[X,X],1))
print(json.dumps({'schema':'gtf84.support-regression/1','status':'success',
 'positive_checks':checks,'negative_controls':negative,'models':summary,
 'complete_symbolic_recovery_example':'d=2,k=4 BB84 measurement, rational nonzero-angle unitary',
 'normalization':'unhalved trace/diamond norm','continuum_theorem_proved_by_tests':False,
 'general_recovery_synthesized':False,'physical_device_executed':False},indent=2,sort_keys=True))
