#!/usr/bin/env python3
"""Exact reset-feedback identities and complete small quantum policy trees.

The scalar amplitudes are rational. Receiver instruments jointly process an
old memory qubit and a new signal; after conditioning, memory is retained.
No assertion in this program purports to prove the continuum theorem.
"""
from fractions import Fraction as F
import copy
import json
from pathlib import Path
from feedback_budget import analyze, canonical, unique_pairs

ROOT=Path(__file__).resolve().parent
count=0
negative=0


def check(ok,message):
    global count
    if not ok:raise RuntimeError(message)
    count+=1


def reject(fn):
    global negative
    try:fn()
    except (ValueError,TypeError):negative+=1;return
    raise RuntimeError('negative control accepted')


def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def tensor(a,b):return tuple(x*y for x in a for y in b)
def matvec(A,v):return tuple(dot(row,v) for row in A)
def transpose(A):return tuple(zip(*A))
def matmul(A,B):return tuple(tuple(dot(row,col) for col in zip(*B)) for row in A)


def instruments(seed):
    # Rational rotations followed by a CNOT and a projective receiver outcome.
    c,d=(F(3,5),F(4,5)) if seed%2 else (F(5,13),F(12,13))
    rotation=((c,-d),(d,c))
    U=tuple(tuple(rotation[i//2][j//2]*(i%2==j%2) for j in range(4)) for i in range(4))
    # CNOT targets the second qubit. Conditioning on the first leaves memory.
    U=tuple(U[2*(i//2)+(i%2)^(i//2)] for i in range(4))
    ops=(U[:2],U[2:])
    completeness=tuple(tuple(sum(K[a][i]*K[a][j] for K in ops for a in range(2))
                            for j in range(4)) for i in range(4))
    check(completeness==tuple(tuple(F(i==j) for j in range(4)) for i in range(4)),
          'receiver instrument is not trace preserving')
    return ops


def tree(N,b,variant=0):
    nodes={}
    def make(name,left,depth):
        if left==0 or (variant%3==1 and depth>0 and name.endswith('1')):
            nodes[name]={'calls':0,'children':[]};return
        n=min(left,b,1+(sum(map(int,name[1:]))+depth+variant)%b)
        children=[name+'0',name+'1']
        nodes[name]={'calls':n,'children':children}
        for child in children:make(child,left-n,depth+1)
    make('r',N,0)
    return nodes


def replay(nodes,s,initial,variant):
    leaves=[]
    def visit(name,u,v):
        node=nodes[name];n=node['calls']
        if not n:leaves.append((u,v));return
        x=F(n)*s
        # A rational pure signal. Its exact root fidelity with |0> is
        # (1-x²)/(1+x²) >= 1-2n²s² on the small replay interval.
        signal0=(F(1),F(0))
        signal1=((1-x*x)/(1+x*x),2*x/(1+x*x))
        check(dot(signal1,signal1)==1,'signal normalization')
        local=abs(dot(signal0,signal1))
        check(local>=1-2*n*n*s*s,'one-block root-fidelity allowance')
        old=abs(dot(u,v))
        a,bv=tensor(u,signal0),tensor(v,signal1)
        check(abs(dot(a,bv))==old*local,'conditional tensor multiplication')
        pairs=[(matvec(K,a),matvec(K,bv)) for K in instruments(len(name)+variant)]
        check(sum(abs(dot(x,y)) for x,y in pairs)>=old*local,'instrument affinity inequality')
        check(sum(dot(x,x) for x,y in pairs)==dot(u,u),'base trace preservation')
        check(sum(dot(y,y) for x,y in pairs)==dot(v,v),'alternative trace preservation')
        for child,(x,y) in zip(node['children'],pairs):visit(child,x,y)
    visit('r',*initial)
    affinity=sum(abs(dot(u,v)) for u,v in leaves)
    check(sum(dot(u,u) for u,v in leaves)==dot(initial[0],initial[0]),'all base leaves complete')
    check(sum(dot(v,v) for u,v in leaves)==dot(initial[1],initial[1]),'all alternative leaves complete')
    # Root overlap is exact also for subnormalized pure receiver states.
    return affinity,len(leaves)


def main():
    examples=[]
    for N in range(1,6):
        for b in range(1,N+1):
            for variant in range(3):
                nodes=tree(N,b,variant)
                data={'schema':'gtf88.reset-policy/1','N':N,'b':b,'s':'1/32','gamma':'2','root':'r','nodes':nodes}
                cert=analyze(data)
                for initial in [((F(1),F(0)),(F(1),F(0))),
                                ((F(3,5),F(4,5)),(F(5,13),F(12,13))),
                                ((F(1,3),F(0)),(F(3,10),F(2,5))),
                                ((F(0),F(0)),(F(1),F(0)))]:
                    overlap,leaves=replay(nodes,F(1,32),initial,variant)
                    lower=F(cert['conditional_product_lower'])*abs(dot(*initial))
                    check(overlap>=lower,'amortized conditional tree lower')
                examples.append({'N':N,'b':b,'variant':variant,'nodes':len(nodes),
                                 'leaves':leaves,'square_cost':cert['square_cost']})
    policy=json.loads((ROOT/'examples/feedback-policy.json').read_text())
    ref=analyze(policy)
    check(ref==analyze(copy.deepcopy(policy)),'deterministic replay')
    check(F(ref['conditional_product_lower'])>=F(ref['conditional_root_fidelity_lower']),
          'product bound dominates additive budget')
    def mutate(key,value):
        obj=copy.deepcopy(policy);obj[key]=value;return obj
    for key,value in [('N',1),('b',0),('b',True),('N',False),('s','2/64'),('s','0'),
                      ('gamma','-1'),('root','missing'),('schema','wrong')]:
        reject(lambda key=key,value=value:analyze(mutate(key,value)))
    obj=copy.deepcopy(policy);obj['nodes']['r']['children']=['r'];reject(lambda:analyze(obj))
    obj=copy.deepcopy(policy);obj['nodes']['r']['children']=['absent'];reject(lambda:analyze(obj))
    obj=copy.deepcopy(policy);obj['nodes']['unused']={'calls':0,'children':[]};reject(lambda:analyze(obj))
    obj=copy.deepcopy(policy);obj['nodes']['r']['children']*=2;reject(lambda:analyze(obj))
    obj=copy.deepcopy(policy);obj['nodes']['r']['calls']=0;reject(lambda:analyze(obj))
    obj=copy.deepcopy(policy);obj['nodes']['r']['calls']=True;reject(lambda:analyze(obj))
    obj=copy.deepcopy(policy);obj['not_a_field']=0;reject(lambda:analyze(obj))
    reject(lambda:analyze(policy,max_nodes=1))
    reject(lambda:json.loads('{"N":1,"N":2}',object_pairs_hook=unique_pairs))
    # Confirm the proof's finite scalar inequalities on a rational mesh,
    # including exact equality and the trivial/saturated regime.
    for q in range(1,9):
        for A in range(q+1):
            for a in range(A+1):
                x,y=F(A,q),F(a,q)
                check((1-(x-y))*(1-y)>=1-x,'backwards induction scalar step')
                check(1-(1-x)**2<=2*x,'trace-from-affinity step')
    print(json.dumps({'schema':'gtf88.feedback-regression/1','status':'success',
      'positive_checks':count,'negative_controls':negative,
      'complete_quantum_policy_replays':4*len(examples),
      'public_policies':examples,'sample_policy_certificate':ref,
      'arithmetic':'exact rational real amplitudes and subnormalized root fidelities',
      'receiver_instruments':'joint memory-signal unitary, projective outcome, retained quantum memory',
      'continuum_theorem_proved_by_tests':False,'physical_protocol_executed':False,
      'general_measurement_lower_protocol_executed':False},indent=2,sort_keys=True))

if __name__=='__main__':main()
