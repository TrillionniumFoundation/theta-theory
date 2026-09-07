#!/usr/bin/env python3
"""Sensitive finite diagnostics, with independent truths and negative controls.

No count below is a continuum theorem certificate. Physical truths use a
separate exponent-keyed algebra, merging actual collisions; the compiler's
input evaluator uses formal labels and never merges them. No old test module
is imported, and no Audit.exact_vectors entry is used as ground truth.
"""
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from finite_compiler import Machine, compile_tables, distance, dyadic
from certified_compiler import (MomentAdvice, formal_labels, verify_program,
                                adaptive_compile)

COUNTS = Counter()
MEASUREMENTS = {}

def check(value, name):
    if not value:
        raise AssertionError(name)
    COUNTS[name] += 1


def powers_product(p,q):
    """Independent univariate exponent algebra; not the author's formal algebra."""
    out = {}
    for x,a in p.items():
        for y,b in q.items():
            out[x+y] = out.get(x+y,F(0))+a*b
    return out


class Truth:
    def __init__(self,gap,shape):
        self.a = (F(0),F(1),F(2)+gap)
        self.shape = F(shape)
        self.cells = ((F(1,3),-F(1,16),-F(1,16)),
                      (F(1,3),F(1,16),F(0)),(F(1,3),F(0),F(1,16)))
        self.grid = tuple(product((F(1,4),F(3,4)),repeat=3))
        self.cache = {}

    def moment(self,alpha):
        return self.shape/(self.shape+sum(a*b for a,b in zip(alpha,self.a)))

    def integral(self,p):
        return sum(c*self.shape/(self.shape+s) for s,c in p.items())

    def posterior_product(self,history):
        if history not in self.cache:
            p = {F(0):F(1)}
            for g,x in history:
                if x < 3:
                    f = {s:g[x]*c for s,c in zip(self.a,self.cells[x])}
                else:
                    f = {s:sum((1-g[j])*self.cells[j][i] for j in range(3))
                         for i,s in enumerate(self.a)}
                p = powers_product(p,f)
            self.cache[history] = p
        return self.cache[history]

    def state(self,history):
        p = self.posterior_product(history)
        z = self.integral(p)
        return tuple(self.integral({s+sum(a*b for a,b in zip(alpha,self.a)):c
                                    for s,c in p.items()})/z
                     for alpha in formal_labels(3-len(history),3))

    def predictions(self,history):
        p = self.posterior_product(history)
        z = self.integral(p)
        factors = ({F(0):F(1,2)}, {F(0):F(1,2),self.a[1]:F(1,32)},
                   {F(0):F(1,2),self.a[2]:F(1,32)})
        result = []
        for word in product(factors,repeat=3-len(history)):
            q = p
            for f in word:
                q = powers_product(q,f)
            result.append(self.integral(q)/z)
        return tuple(result)

    def actual(self,history):
        return tuple((self.grid[u],x) for u,x in history)


def noisy_advice(truth,bits):
    delta = F(1,1<<(bits+26))
    def perturb(v,i):
        # Rounded true value plus a signed perturbation, all dyadic; <=delta/2.
        return dyadic((v,),bits+29)[0]+(delta/4 if i%2 else -delta/4)
    cells = tuple(tuple(perturb(v,3*j+i) for i,v in enumerate(row))
                  for j,row in enumerate(truth.cells))
    all_labels = tuple(a for n in range(4) for a in formal_labels(n,3))
    moments = {a:perturb(truth.moment(a),i) for i,a in enumerate(all_labels)}
    for row,original in zip(cells,truth.cells):
        for value,v in zip(row,original):
            check(abs(value-v)<=delta,'coefficient_input_budget')
    for a,v in moments.items():
        check(abs(v-truth.moment(a))<=delta,'moment_input_budget')
    if truth.a[2] == 2:
        # Equal exact exponent sums have deliberately unequal advice entries.
        broken = sum(moments[a]!=moments[b] for a in all_labels for b in all_labels
                     if a!=b and sum(x*y for x,y in zip(a,truth.a)) ==
                     sum(x*y for x,y in zip(b,truth.a)))
        check(broken>0,'exact_collision_numerical_equality_broken')
    return MomentAdvice(cells,moments,truth.grid,3,delta,F(2),F(1,32))


def output_failures(program,audit,predict,tol,nonconstant_only=False):
    failed = total = 0
    for n,stage in enumerate(audit.representatives):
        for i,hist in enumerate(stage):
            exact = predict(hist)
            for q,value in enumerate(exact):
                if nonconstant_only and q == 0:
                    continue
                total += 1
                observed = F(program.outputs[n][i][q],1<<program.output_bits)
                failed += abs(observed-value)>tol
    return failed,total


def physical_tests():
    receipts = []
    rng = random.Random(110609)
    max_query_bound = F(0)
    maximum_actual_error = F(0)
    all_zero_detections = nonconstant_detections = 0
    for gap,shape in ((F(0),1),(F(1,10**12),1),(F(1,7),3)):
        truth = Truth(gap,shape)
        for M in (1,2,4):
            bits = 12
            tau = F(1,1<<bits)
            advice = noisy_advice(truth,bits)
            program,audit = compile_tables(2,8,4,M,bits,advice.state,advice.predictions)
            check(advice.max_quotient_bound <= tau/4,'certified_input_quotient_budget')
            check(advice.min_denominator >= F(1,32)**2/2,'positive_perturbed_evidence')
            check(program.state_counts[0]==1 and max(program.state_counts)<=M,'persistent_M_budget')
            check(Machine.__slots__==('index',),'index_only_runtime')
            check(not hasattr(program,'representatives') and not hasattr(program,'evaluate'),
                  'no_runtime_history_or_oracle')
            # Check every offline representative's raw coordinate and all queries
            # against the independently integrated, unperturbed true experiment.
            for n,stage in enumerate(audit.representatives):
                for hist in stage:
                    actual = truth.actual(hist)
                    raw = advice.state(hist)
                    for value,exact in zip(raw,truth.state(actual)):
                        check(abs(value-exact)<=tau/4,'independent_raw_advice_truth')
                    for value,exact in zip(advice.predictions(hist),truth.predictions(actual)):
                        check(abs(value-exact)<=tau/4,'independent_query_advice_truth')
            failed,total = output_failures(program,audit,lambda h:truth.predictions(truth.actual(h)),tau)
            check(failed==0,'all_stored_outputs_accurate')
            COUNTS['stored_query_entries_checked'] += total
            zero = replace(program,outputs=tuple(tuple(tuple(0 for q in row) for row in stage)
                                                  for stage in program.outputs))
            corrupt = replace(program,outputs=tuple(tuple(tuple(v if q==0 else 0 for q,v in enumerate(row))
                                                        for row in stage) for stage in program.outputs))
            bad,count = output_failures(zero,audit,lambda h:truth.predictions(truth.actual(h)),tau)
            check(bad==count and count>0,'zero_output_negative_control')
            all_zero_detections += bad
            bad,count = output_failures(corrupt,audit,lambda h:truth.predictions(truth.actual(h)),tau,True)
            check(bad==count and count>0,'nonconstant_decoder_negative_control')
            nonconstant_detections += bad
            # Valid sharp fixture constants: accepted command multiplier cancels;
            # their state constant <=22/5. Failure l1<=13/16 and evidence>=1/4
            # give L<=13/2; pointwise command change<=||dg|| gives G<=8.
            mesh = F(1,2048)
            residuals = verify_program(program,audit,8,4,advice.state,advice.predictions,
                                       tau,mesh,(F(13,2),)*2,(F(8),)*2,(F(1),)*3)
            badres = verify_program(zero,audit,8,4,advice.state,advice.predictions,
                                    tau,mesh,(F(13,2),)*2,(F(8),)*2,(F(1),)*3)
            check(max(residuals.output)<2*tau,'sensitive_decoder_residual')
            check(max(badres.output)>F(1,2),'corrupted_decoder_residual_detected')
            for n in (1,2):
                check(residuals.query_error[n]<F(1,2),'informative_physical_bound_below_half')
                max_query_bound = max(max_query_bound,residuals.query_error[n])
            for word in range(48):
                actual = ()
                machine = Machine()
                for n in range(2):
                    u = rng.randrange(8)
                    g = tuple(v+(mesh if v==F(1,4) else -mesh) for v in truth.grid[u])
                    x = rng.randrange(4)
                    actual += ((g,x),)
                    machine.step(program,n,u,x)
                    exact = truth.predictions(actual)
                    for q,value in enumerate(exact):
                        error = abs(machine.output(program,n+1,q)-value)
                        check(error<=residuals.query_error[n+1],'all_query_offgrid_end_to_end')
                        maximum_actual_error = max(maximum_actual_error,error)
                    representative = truth.actual(audit.representatives[n+1][machine.index])
                    check(distance(truth.state(actual),truth.state(representative))<=residuals.state_error[n+1],
                          'informative_offgrid_state_recurrence')
            receipts.append({'gap':str(gap),'prior_shape':shape,'M':M,
                             'state_counts':program.state_counts,'input_delta':str(advice.delta),
                             'max_quotient_certificate':str(advice.max_quotient_bound),
                             'state_bounds':list(map(str,residuals.state_error)),
                             'query_bounds':list(map(str,residuals.query_error))})
    MEASUREMENTS.update(physical_programs=receipts,zero_output_entries_detected=all_zero_detections,
                        nonconstant_entries_detected=nonconstant_detections,
                        max_physical_query_bound=str(max_query_bound),
                        max_physical_actual_query_error=str(maximum_actual_error))


def adaptive_tests():
    receipts = []
    # S_n is an interval of length (1/2)(1-2^-n); e_n(M) is known exactly.
    for T,M in ((1,1),(1,2),(1,4),(2,1),(2,2)):
        A = 1-F(1,2**T)
        def factory(b,tau):
            segments = max(1,1<<(max(0,b-2)))
            grid = tuple(F(1,4)+F(j,2*segments) for j in range(segments+1))
            cache = {}
            def exact(h):
                s = F(1,2)
                for u,x in h:
                    s = (s+grid[u])/2
                return s
            def evaluate(h):
                if h not in cache:
                    sign = 1 if sum(u for u,x in h)%2 else -1
                    cache[h] = (exact(h)+sign*tau/8,)
                return cache[h]
            def predict(h):
                s = exact(h)
                return (s+tau/8,s*s-tau/8,(1+s)/2+tau/8)
            return len(grid),evaluate,predict,(grid,exact,evaluate,predict)
        p,a,stages,meta = adaptive_compile(T,1,M,A,factory,max_candidates=200000)
        e = A/(4*M)
        for item in stages:
            check(item['lower']<=e<=item['upper'],'adaptive_certificate_exact_interval_oracle')
        last = stages[-1]; h,r = last['h'],last['r']; c = A+2
        check(r>=4*c*h,'adaptive_stopping_rule')
        check(3*r/8<=e<=5*r/4,'adaptive_final_two_sided_bracket')
        check(e/(10*c)<h<=e/(2*c-1),'adaptive_precision_scale')
        check(last['b']>0 and all(not item['radius_stop'] for item in stages[:-1]),'adaptive_first_success')
        check(max(p.state_counts)<=M,'adaptive_exact_M_budget')
        grid,exact,evaluate,predict = meta
        residue = verify_program(p,a,len(grid),1,evaluate,predict,h/8,h,(F(1,2),)*T,
                                 (F(1,2),)*T,(F(3,2),)*(T+1))
        for n in range(1,T+1):
            check(residue.query_error[n]<1,'adaptive_informative_query_bound')
        # Exhaustive off-grid words from a four-point domain, not the synthesis grid.
        values = (F(5,17),F(7,17),F(9,17),F(11,17))
        for word in product(values,repeat=T):
            s = F(1,2); machine = Machine()
            for n,u in enumerate(word):
                ui = min(range(len(grid)),key=lambda j:(abs(grid[j]-u),j))
                check(abs(u-grid[ui])<=h,'adaptive_input_name_accuracy')
                s = (s+u)/2
                machine.step(p,n,ui,0)
                for q,v in enumerate((s,s*s,(1+s)/2)):
                    check(abs(machine.output(p,n+1,q)-v)<=residue.query_error[n+1],
                          'adaptive_all_query_causal_output')
        receipts.append({'T':T,'M':M,'true_cover_radius':str(e),
                         'stages':[{k:str(v) if isinstance(v,F) else v for k,v in z.items()} for z in stages]})
    # The absolute-tolerance branch must terminate on e(M)=0; no equality test.
    def constant_factory(b,tau):
        return 1,lambda h:(F(1,2),),lambda h:(F(1,2),),None
    p,a,stages,_ = adaptive_compile(2,1,1,F(0),constant_factory,F(1,32))
    check(stages[-1]['h']==F(1,32) and not stages[-1]['radius_stop'],'zero_radius_absolute_tolerance')
    MEASUREMENTS['adaptive_fixtures'] = receipts


def separated_floor_tests():
    for a in ((F(0),F(1)),(F(0),F(1),F(2)),(F(0),F(1),F(2)+F(1,10**9),F(3))):
        r,D = len(a),a[-1]
        gap = min(y-x for x,y in zip(a,a[1:]))
        for N in range(2,8):
            k=N//2;m=N-k;d=(r-1)*k;H=N*D
            chain=sorted({j*D for j in range(m+1)}|{j*D+x for j in range(m) for x in a[1:-1]})
            check(len(chain)==m*(r-1)+1,'separated_chain_cardinality')
            check(min(y-x for x,y in zip(chain,chain[1:]))>=gap,'separated_chain_gap')
            nodes=chain[1:1+d]
            volume=F(1)
            for i in range(d):
                for j in range(i):volume*=(nodes[i]-nodes[j])/H
            check(volume>0 and volume>=(gap/H)**(d*(d-1)//2),'separated_chain_volume')
            for M in (1,2,7,64,1000):
                b=0
                while (1<<(b*d))<M+1:b+=1
                check(F(1,1<<b)**(2*d)<=F(1,M*M),'sufficient_precision_integer_rule')


def main():
    physical_tests();adaptive_tests();separated_floor_tests()
    receipt={'status':'passed','assertions':sum(COUNTS.values()),'categories':dict(COUNTS),
             'measurements':MEASUREMENTS,
             'scope':'Finite rational diagnostics and deliberate negative controls; not a continuum proof, a precision/program converse, exhaustive priority search, or journal approval.'}
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'validation/V11_DIAGNOSTICS.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='measurements'},indent=2))

if __name__=='__main__':main()
