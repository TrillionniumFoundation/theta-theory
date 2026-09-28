"""Finite exact regressions for v59. No universal theorem is certified by tests."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import qubit_compiler as q

COUNT=0
NEG=[]
def check(ok,message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)
def refuses(name,fn):
    try:fn()
    except (ValueError,RuntimeError,TypeError,ZeroDivisionError):NEG.append(name);return
    raise RuntimeError('undetected negative control: '+name)
def reject_unless(ok):
    if not ok:raise ValueError('intended refusal')
def squared(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def tv(a,b):return sum(abs(a.get(k,F(0))-b.get(k,F(0))) for k in set(a)|set(b))/2

def true_law(commands,seed,probes,n,policy):
    states={((),seed):F(1)}
    for t in range(n):
        nxt={}
        for (hist,x),mass in states.items():
            for control,cp in policy(hist,t):
                if control in commands:
                    events=[(-1,F(1),q.apply(commands[control],x))]
                else:events=[(y,out['bias']+q.dot(out['linear'],x),x) for y,out in enumerate(probes[control])]
                for y,p,z in events:
                    key=(hist+((control,y),),z);nxt[key]=nxt.get(key,F(0))+mass*cp*p
        states=nxt
    out={}
    for (hist,_),mass in states.items():out[hist]=out.get(hist,F(0))+mass
    return out

def machine_law(data,n,policy,rounded=True):
    rows=data['rows' if rounded else 'exact_rows']
    emits=data['emissions' if rounded else 'exact_emissions']
    states={((),data['initial_label']):F(1)}
    for t in range(n):
        nxt={}
        for (hist,z),mass in states.items():
            for control,cp in policy(hist,t):
                events=[(-1,p,i) for i,p in rows[control][z]] if control in rows else [(y,p,z) for y,p in emits[control][z]]
                for y,p,i in events:
                    key=(hist+((control,y),),i);nxt[key]=nxt.get(key,F(0))+mass*cp*p
        states=nxt
    out={}
    for (hist,_),mass in states.items():out[hist]=out.get(hist,F(0))+mass
    return out

def main():
    home=Path(__file__).resolve().parent
    raw=json.loads((home/'GENERIC_INPUT.json').read_text())
    commands,seed,probes,eta=q.supplied_input(raw)
    check(seed==(F(3,5),F(4,5),F(0)),'generic seed identity')
    check(set(commands)=={'hold','quarter'},'generic alphabet identity')
    exact=q.compile_exact(2,F(1,2),commands=commands,seed=seed,max_labels=100)
    check(exact['labels']<=53 and exact['vertices'][exact['initial_label']]==seed,'generic net initialization')
    for name,rows in exact['rows'].items():
        for v,row in zip(exact['vertices'],rows):
            check(q.valid_row(exact['vertices'],row,q.scale(exact['contraction'],q.apply(commands[name],v))), 'generic terminal row')
    for word in product(commands,repeat=2):
        dist={exact['initial_label']:F(1)};x=seed
        for name in word:
            new={}
            for i,mass in dist.items():
                for j,p in exact['rows'][name][i]:new[j]=new.get(j,F(0))+mass*p
            dist=new;x=q.apply(commands[name],x)
        mean=tuple(sum((p*exact['decoder_bloch'][i][d] for i,p in dist.items()),F(0)) for d in range(3))
        check(mean==q.scale(F(1,2),x),'generic terminal exact word')
    data=q.compile_causal(3,F(1,2),commands=commands,seed=seed,probes=probes,eta=eta,max_labels=100)
    check(data['m']==2 and data['max_row_support']<=4,'process size/support')
    check(data['kl_upper_bound']<=F(1,8),'process half-budget KL')
    check(data['rounding_path_tv_bound']<=F(1,4),'process rounding half-budget')
    check(not data['spectral_gap_certified'] and not data['universal_process_theorem_certified_by_tests'],'proof/test distinction')
    vertices=data['vertices'];r=data['contraction'];b=data['fair_bits_per_control']
    targets=[seed,q.E1,*[q.scale(F(-1),v) for v in [seed,q.E1]]]
    for name,rows in data['exact_rows'].items():
        for i,(v,row) in enumerate(zip(vertices,rows)):
            check(q.valid_row(vertices,row,q.scale(r,q.apply(commands[name],v))),'causal exact row')
            rounded=dict(data['rows'][name][i]);unrounded=dict(row)
            check(sum(rounded.values(),F(0))==1 and min(rounded.values())>=0,'dyadic stochasticity')
            check(all((1<<b)%p.denominator==0 for p in rounded.values()),'dyadic denominator')
            check(tv(rounded,unrounded)<=F(3,1<<b),'dyadic local budget')
            for x in targets:
                lhs=sum((p*squared(vertices[j],q.apply(commands[name],x)) for j,p in row),F(0))
                check(lhs<=r*squared(v,x)+2*(1-r),'unit-or-zero conditional second moment')
    for name,rows in data['exact_emissions'].items():
        for i,row in enumerate(rows):
            check(sum((p for _,p in row),F(0))==1 and min(p for _,p in row)>=eta,'probe positivity')
            check(tv(dict(row),dict(data['emissions'][name][i]))<=F(len(row)-1,1<<b),'probe rounding')
    controls=list(commands)+list(probes)
    max_actual=F(0)
    policies=[]
    for word in product(controls,repeat=3):
        policies.append(lambda hist,t,w=word:[(w[t],F(1))])
    # Policies see public history, not the simulator's private label.
    policies += [lambda h,t:[('probe1' if t==0 else ('quarter' if h[0][1]==0 else 'hold') if t==1 else 'probe2',F(1))],
                 lambda h,t:[(controls[(t+sum(y for _,y in h if y>=0))%len(controls)],F(1,3)),('probe3',F(2,3))]]
    for policy in policies:
        p=true_law(commands,seed,probes,3,policy)
        e=machine_law(data,3,policy,False);d=machine_law(data,3,policy,True)
        check(sum(p.values(),F(0))==sum(e.values(),F(0))==sum(d.values(),F(0))==1,'full transcript normalization')
        err=tv(p,d);max_actual=max(max_actual,err)
        check(err<=F(1,2),'whole-path adaptive TV')
        check(tv(e,d)<=data['rounding_path_tv_bound'],'instrument perturbation on full path')
    free=q.compile_causal(3,F(1,2),max_labels=100)
    for word in [('U','V','probe2'),('V','U','probe2'),('U*','V','probe3')]:
        policy=lambda hist,t,w=word:[(w[t],F(1))]
        law=machine_law(free,3,policy,False)
        x=q.apply(free['commands'][word[1]],q.apply(free['commands'][word[0]],q.E1))
        affine=free['probes'][word[2]][0]
        expected=affine['bias']+free['contraction']**2*q.dot(affine['linear'],x)
        actual=sum((mass for hist,mass in law.items() if hist[-1][1]==0),F(0))
        check(actual==expected,'noncommuting chronological causal mean')
    def free_adaptive(hist,t):
        return [('probe1' if t==0 else ('U' if hist[0][1]==0 else 'V') if t==1 else 'probe3',F(1))]
    check(tv(true_law(free['commands'],q.E1,free['probes'],3,free_adaptive),
             machine_law(free,3,free_adaptive))<=F(1,2),'free-alphabet adaptive transcript')
    for m in range(2,8):
        for k in range(1,m):
            # Each label gives a probability row on m disjoint testing events.
            rows=[[F((i+j)%m+1,m*(m+1)//2) for j in range(m)] for i in range(k)]
            check(sum(max(row[j] for row in rows) for j in range(m))<=k,'disjoint-testing mixture bound')
    for length in range(1,10):
        iid={w:F(1,2**length) for w in product([0,1],repeat=length)}
        correlated={(0,)*length:F(1,2),(1,)*length:F(1,2)}
        check(tv(iid,correlated)==1-F(1,2**(length-1)),'correct marginals are not a process law')
    for t in range(1,12):
        check(3**t>=1 and 2*3**t-1==1+4*sum(3**j for j in range(t)),'free-ball finite count')
        check(F(1,25**t)>F(2,3)*F(1,25**t),'disjoint empirical coordinate radii')
    refuses('float-rational',lambda:q.rational(0.5))
    refuses('non-orthogonal-command',lambda:q.validate_geometry({'bad':((1,1,0),(0,1,0),(0,0,1))}))
    refuses('reflection-not-SO3',lambda:q.validate_geometry({'bad':((-1,0,0),(0,1,0),(0,0,1))}))
    refuses('interior-seed',lambda:q.validate_geometry(commands,(F(1,2),0,0)))
    refuses('empty-alphabet',lambda:q.validate_geometry({}))
    refuses('nonpositive-probe-floor',lambda:q.validate_probes(probes,0,commands))
    refuses('negative-ball-probe',lambda:q.validate_probes({'p':[{'bias':'1/2','linear':[1,0,0]},{'bias':'1/2','linear':[-1,0,0]}]},F(1,4),commands))
    refuses('unnormalized-probe',lambda:q.validate_probes({'p':[{'bias':'3/4','linear':[0,0,0]}]},F(1,4),commands))
    refuses('uncancelled-linear-probe',lambda:q.validate_probes({'p':[{'bias':'1/2','linear':['1/8',0,0]},{'bias':'1/2','linear':[0,0,0]}]},F(1,4),commands))
    refuses('colliding-control-names',lambda:q.validate_probes({'hold':probes['probe1']},eta,commands))
    refuses('allocation-limit',lambda:q.compile_causal(100,F(1,10),max_labels=100))
    refuses('zero-process-error',lambda:q.compile_causal(1,0))
    refuses('unit-process-error',lambda:q.compile_causal(1,1))
    refuses('negative-horizon',lambda:q.compile_causal(-1,F(1,2)))
    refuses('unknown-schema',lambda:q.supplied_input(dict(raw,schema='wrong')))
    refuses('unknown-field',lambda:q.supplied_input(dict(raw,private_history=True)))
    refuses('fake-gap-claim',lambda:reject_unless(data['spectral_gap_certified']))
    refuses('fake-universal-check',lambda:reject_unless(data['universal_process_theorem_certified_by_tests']))
    # The interior-seed shortcut would violate the claimed one-step second moment.
    refuses('false-interior-variance-shortcut',lambda:reject_unless(2-r<=r*F(1,4)+2*(1-r)))
    refuses('marginals-as-path-certification',lambda:reject_unless(1-F(1,128)<=F(1,4)))
    refuses('unbudgeted-local-rounding',lambda:reject_unless(F(3*3,2)<=F(1,4)))
    refuses('wrong-contracted-mean',lambda:reject_unless(q.valid_row(vertices,data['exact_rows']['quarter'][1],q.apply(commands['quarter'],vertices[1]))))
    print(json.dumps({'status':'success','exact_finite_assertions':COUNT,'negative_controls_detected':NEG,
        'generic_terminal_labels':exact['labels'],'generic_causal_labels':data['labels'],
        'adaptive_and_fixed_policies_checked':len(policies),'max_checked_path_tv':str(max_actual),
        'scope':'finite rational row, variance, joint-transcript and refusal regressions; not proof of universal causal classification',
        'spectral_gap_certified':False,'universal_theorems_certified':False},sort_keys=True))

if __name__=='__main__':main()
