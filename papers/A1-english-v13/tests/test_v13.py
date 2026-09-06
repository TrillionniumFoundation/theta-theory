#!/usr/bin/env python3
"""Request-conformance mutations and one-name physical collision diagnostics.

Ground truth uses exponent-keyed algebra and exact rational prior integrals,
not compiler representatives or residuals. The physical execution domain is a
complete finite two-command subexperiment, not the continuum command cube.
"""
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import certified_compiler as cc
from construction_contracts import bind_request, inspect_construction, ContractError
from finite_compiler import Machine
from test_v11 import Truth, powers_product
from test_v12 import exact_finite_cover_radius, norm
COUNTS=Counter();RESULTS={}

def check(ok,category):
    if not ok:raise AssertionError(category)
    COUNTS[category]+=1

def interval_factory(b,h,tau=None):
    segments=max(1,1<<max(0,b-2))
    grid=tuple(F(1,4)+F(j,2*segments) for j in range(segments+1))
    def state(hist):
        s=F(1,2)
        for u,_ in hist:s=(s+grid[u])/2
        return (s,)
    return len(grid),state,state,grid

def finite_factory(b,h,tau=None):
    grid=(F(1,4),F(1,2),F(3,4))
    def state(hist):
        s=F(1,2)
        for u,_ in hist:s=(s+grid[u])/2
        return (s,)
    return len(grid),state,state,grid

def invoke(routine,T,M,factory,A):
    kw={'state_dimensions':(1,)*(T+1),'query_counts':(1,)*(T+1)}
    if routine=='ordinary':
        return cc.adaptive_compile(T,1,M,A,factory,absolute_tolerance=F(1,128),max_bits=12,**kw)
    return cc.robust_adaptive_compile(T,1,M,A,factory,F(1,128),max_bits=12,**kw)

def conformance_mutations():
    original=cc.compile_tables;rows=[]
    try:
        for routine in ('ordinary','robust'):
            for M in (1,2):
                cc.compile_tables=original
                p,a,trace,grid=invoke(routine,1,M,interval_factory,F(1,2))
                e=F(1,8*M)
                for t in trace:
                    check(t['lower']<=e<=t['upper'],'nominal_known_continuum_radius_bracket')
                    check(t['bound_total_error']<=max(t['h'],F(1,128)),
                          'bound_request_error_budget')
                check(p.output_bits==trace[-1]['requested_bits'],'nominal_bound_precision')
                rows.append({'routine':routine,'M':M,'fault':'none','true_radius':e,
                             'trace':trace,'max_query_error':max(abs(F(p.outputs[1][
                             p.transitions[0][0][u][0]][0],1<<p.output_bits)-
                             (F(1,2)+grid[u])/2) for u in range(len(grid)))})
                for fault in ('coarse_bits','lying_bits','lying_bits_rescaled',
                              'query_truncation','query_value_corruption',
                              'collapse'):
                    counter={'calls':0,'changed':0}
                    def broken(*args,**kw):
                        counter['calls']+=1
                        aa=list(args);requested=aa[4]
                        if fault in ('coarse_bits','lying_bits','lying_bits_rescaled'):
                            aa[4]=0;p,a=original(*aa,**kw)
                            if fault=='lying_bits':p=replace(p,output_bits=requested)
                            if fault=='lying_bits_rescaled':
                                outputs=tuple(tuple(tuple(x*(1<<requested) for x in row)
                                                    for row in stage) for stage in p.outputs)
                                p=replace(p,output_bits=requested,outputs=outputs)
                        elif fault=='coarse_state_truthful_queries':
                            evaluator=aa[5];aa[5]=lambda h:tuple(F(round(v)) for v in evaluator(h))
                            p,a=original(*aa,**kw)
                        else:
                            p,a=original(*aa,**kw)
                            if fault=='query_truncation':
                                p=replace(p,outputs=tuple(tuple(()) for _ in p.outputs))
                            elif fault=='query_value_corruption':
                                # The one-query fixture uses a false numerical value rather than
                                # a vacuous permutation; genuine multi-query swaps are checked below.
                                p=replace(p,outputs=tuple(tuple(tuple((x+1)%(1+(1<<p.output_bits))
                                              for x in row) for row in stage) for stage in p.outputs))
                            else:
                                trans=tuple(tuple(tuple(tuple(0 for _ in xs) for xs in us)
                                                   for us in stage) for stage in p.transitions)
                                counter['changed']+=sum(j!=0 for st in p.transitions for us in st for xs in us for j in xs)
                                p=replace(p,transitions=trans)
                        return p,a
                    # Collapse cannot change a one-label transducer; record the genuine M=2 case only.
                    if fault=='collapse' and M==1:continue
                    cc.compile_tables=broken
                    try:invoke(routine,1,M,interval_factory,F(1,2))
                    except ContractError as err:
                        check(True,'adaptive_gate_rejects_'+fault)
                        rows.append({'routine':routine,'M':M,'fault':fault,'rejected':True,
                                     'rejection':str(err),'true_radius_unchanged':e,**counter})
                    else:raise AssertionError('fault returned a program: '+routine+'/'+fault)
            for fault in ('short_horizon','padded_horizon','state_count_metadata','query_swap'):
                def broken(*args,**kw):
                    aa=list(args)
                    if fault in ('short_horizon','padded_horizon'):
                        aa[0]=1;p,a=original(*aa,**kw)
                        if fault=='padded_horizon':
                            # Append copied tables and audit metadata; histories still have wrong lengths.
                            p=replace(p,transitions=p.transitions+(p.transitions[-1],),
                                      outputs=p.outputs+(p.outputs[-1],),
                                      state_counts=p.state_counts+(p.state_counts[-1],))
                            a=replace(a,representatives=a.representatives+(a.representatives[-1],))
                    elif fault=='state_count_metadata':
                        p,a=original(*aa,**kw)
                        p=replace(p,state_counts=(1,1,1))
                    else:
                        p,a=original(*aa,**kw)
                        p=replace(p,outputs=tuple(tuple(tuple(reversed(row)) for row in st) for st in p.outputs))
                    return p,a
                cc.compile_tables=broken
                if fault=='query_swap':
                    def factory(b,h,tau=None):
                        c,e,q,meta=finite_factory(b,h,tau)
                        return c,e,lambda hist:(F(1,8),F(7,8)),meta
                    def run():
                        if routine=='ordinary':
                            return cc.adaptive_compile(2,1,2,F(0),factory,absolute_tolerance=F(1,128),
                                                       state_dimensions=(1,1,1),query_counts=(2,2,2))
                        return cc.robust_adaptive_compile(2,1,2,F(0),factory,F(1,128),
                                                         state_dimensions=(1,1,1),query_counts=(2,2,2))
                else:
                    def run():return invoke(routine,2,2,finite_factory,F(0))
                try:run()
                except (ContractError,) as err:
                    check(True,'structural_gate_rejects_'+fault)
                    rows.append({'routine':routine,'fault':fault,'rejected':True,'rejection':str(err)})
                else:raise AssertionError('structural mutation accepted: '+fault)
    finally:cc.compile_tables=original
    # A change to unused internal audit vectors can leave exactly the same
    # valid finite construction. Acceptance is intentionally extensional.
    c,e,q,_=finite_factory(4,F(1,16))
    req,name=bind_request(1,c,1,1,6,e,q,F(0),F(1,64))
    p,a=original(1,c,1,1,6,lambda h:tuple(F(round(v)) for v in e(h)),q)
    cert=inspect_construction(p,a,c,1,1,name.evaluate,name.predict,request=req).require()
    check(cert.accepted and cert.radii[1]==F(1,4),'construction_equivalent_internal_change_accepted')
    for schema in ('states','queries'):
        try:
            bind_request(1,c,1,2,6,e,q,F(0),F(1,64),
                         state_dimensions=(2,2) if schema=='states' else (1,1),
                         query_counts=(2,2) if schema=='queries' else (1,1))
        except ContractError:check(True,'external_'+schema+'_schema_mismatch_rejected')
        else:raise AssertionError('external schema mismatch accepted')
    # A malformed external error budget is rejected without invoking synthesis.
    c,e,q,_=finite_factory(4,F(1,16))
    try:bind_request(1,c,1,2,0,e,q,F(1,32),F(1,16))
    except ContractError:check(True,'rounding_plus_raw_exceeds_budget_rejected')
    else:raise AssertionError('incompatible external rounding budget accepted')
    # Frozen data have no mutable dict exposed to the compiler.
    req,name=bind_request(1,c,1,2,6,e,q,F(0),F(1,64))
    try:name.states[()]=(F(0),)
    except TypeError:check(True,'frozen_numerical_name_immutable')
    else:raise AssertionError('frozen name mutated')
    p,a=original(1,c,1,2,6,name.evaluate,name.predict)
    try:inspect_construction(p,a,c,1,2,lambda h:(F(0),),name.predict,request=req)
    except ContractError:check(True,'changed_external_name_rejected')
    else:raise AssertionError('changed name accepted')
    RESULTS['request_conformance']=rows


class TiltedTruth(Truth):
    """Uniform reference prior tilted by 1+epsilon*(t-1/2).

    Integrals are computed at actual exponents. No formal moment evaluator,
    compiler rounding or selected representative is used as physical truth.
    """
    def __init__(self,gap,epsilon):
        super().__init__(gap,1);self.epsilon=F(epsilon)
    def one_moment(self,s):
        return F(1,s+1)+self.epsilon*(F(1,s+2)-F(1,2*(s+1)))
    def moment(self,alpha):
        return self.one_moment(sum(a*b for a,b in zip(alpha,self.a)))
    def integral(self,p):
        return sum(c*self.one_moment(s) for s,c in p.items())


def physical_common_name():
    delta=F(1,1<<26)
    commands=((F(1,4),F(3,4),F(1,4)),(F(3,4),F(1,4),F(3,4)))
    center=TiltedTruth(F(0),F(0));center.grid=commands
    labels=tuple(a for d in range(4) for a in cc.formal_labels(d,3))
    # One rational table, fixed throughout every refinement and in every model.
    moments={a:center.moment(a)+(delta/8 if i%2 else -delta/8) for i,a in enumerate(labels)}
    models=[TiltedTruth(gap,eps) for gap,eps in
            ((F(0),delta/2),(F(0),-delta/2),(-delta/4,F(0)),(delta/4,F(0)))]
    for truth in models:truth.grid=commands
    advice=cc.MomentAdvice(center.cells,moments,commands,3,delta,F(2),F(1,32))
    for u in range(2):
        for x in range(4):
            coeff=advice.factor(u,x)
            check(sum(abs(v) for v in coeff)<=1,'physical_factor_coefficient_norm')
            check(coeff[0]+sum(min(F(0),v) for v in coeff[1:])>=F(1,32),
                  'physical_positive_likelihood_bound')
    alphabet=tuple(product(range(2),range(4)))
    histories=[tuple(product(alphabet,repeat=n)) for n in range(3)]
    physical_inputs=[]
    max_error=F(0)
    for truth in models:
        discrepancy=max(abs(moments[a]-truth.moment(a)) for a in labels)
        check(discrepancy<=delta,'single_moment_name_compatible_with_physical_model')
        se=qe=F(0)
        for hs in histories:
            for h in hs:
                actual=truth.actual(h)
                se=max(se,norm(advice.state(h),truth.state(actual)))
                qe=max(qe,norm(advice.predictions(h),truth.predictions(actual)))
        max_error=max(max_error,se,qe)
        physical_inputs.append({'gap':truth.a[2]-2,'prior_tilt':truth.epsilon,
                                'moment_discrepancy':discrepancy,'state_name_error':se,'query_name_error':qe})
    # General finite-moment certificate, not fitted to the returned transducer.
    rho=2*advice.max_quotient_bound
    check(0<rho<=1,'analytic_common_floor_in_range')
    check(max_error<=rho/2,'all_models_raw_callback_error_within_common_floor')
    fixed_table_digest=hashlib.sha256(repr(tuple(moments.items())).encode()).hexdigest()
    results=[]
    for M in (1,2,4):
        calls=[]
        def factory(b,h,tau):
            check(advice.max_quotient_bound<=tau/2,'common_physical_external_error_certificate')
            check(hashlib.sha256(repr(tuple(moments.items())).encode()).hexdigest()==fixed_table_digest,
                  'same_moment_table_at_every_scale')
            calls.append({'b':b,'h':h,'tau':tau,'moment_name_sha256':fixed_table_digest})
            return 2,advice.state,advice.predictions,advice
        p,a,trace,_=cc.robust_adaptive_compile(2,4,M,F(0),factory,rho,max_bits=22,
                                               state_dimensions=(10,6,3),query_counts=(27,9,3))
        digest=hashlib.sha256(repr(p).encode()).hexdigest()
        last=trace[-1];tau=last['tau']
        request,name=bind_request(2,2,4,M,last['b']+2,advice.state,advice.predictions,tau/2,tau,
                                 state_dimensions=(10,6,3),query_counts=(27,9,3))
        cert=inspect_construction(p,a,2,4,M,name.evaluate,name.predict,request=request).require()
        E=[F(0)]
        # All acquisition factor coefficient l1 norms are <=1 and their
        # pointwise lower bounds exceed 1/32 (checked before synthesis).
        # The normalized raw-moment quotient therefore has L <=2/(1/32)=64.
        for n in range(2):E.append(64*E[-1]+cert.radii[n+1]+2*tau)
        rows=[]
        for truth in models:
            es=tuple(exact_finite_cover_radius((truth.state(truth.actual(h)) for h in histories[n]),M)
                     for n in (1,2))
            e=max(es)
            for t in trace:check(t['lower']<=e<=t['upper'],'common_physical_exact_radius_bracket')
            check(last['h']>(e+rho)/42 and last['h']<=e+rho,
                  'common_physical_selected_scale_for_each_model')
            err=F(0);path_count=0
            for hist in histories[2]:
                machine=Machine();prefix=()
                for n,(u,x) in enumerate(hist):
                    machine.step(p,n,u,x);prefix+=((u,x),)
                    actual=truth.actual(prefix)
                    rep=truth.actual(a.representatives[n+1][machine.index])
                    check(norm(truth.state(actual),truth.state(rep))<=E[n+1],
                          'one_table_physical_state_recurrence')
                    for q,target in enumerate(truth.predictions(actual)):
                        discrepancy=abs(machine.output(p,n+1,q)-target)
                        err=max(err,discrepancy)
                        check(discrepancy<=E[n+1]+tau,'one_table_all_physical_query_errors')
                path_count+=1
            check(hashlib.sha256(repr(p).encode()).hexdigest()==digest,
                  'identical_program_executed_against_every_model')
            rows.append({'gap':truth.a[2]-2,'prior_tilt':truth.epsilon,'program_sha256':digest,
                         'true_stage_radii':es,'true_radius':e,'maximum_query_error':err,
                         'paths':path_count,'state_bounds':E,'query_bounds':[v+tau for v in E]})
        results.append({'M':M,'one_program_sha256':digest,'state_counts':p.state_counts,
                        'moment_name_sha256':fixed_table_digest,'requested_schema':
                        {'horizon':2,'state_dimensions':[10,6,3],'query_counts':[27,9,3]},
                        'stopping_trace':trace,'input_trace':calls,'models':rows})
    # Exact physical realization of the future basis. The finite acquisition
    # alphabet lies inside the eta=1/8 cube. The query command uses rejection
    # coordinates (1/3,5/6,1/3), also inside that same cube.
    for j in (1,2):
        rejection=[F(1,3)]*3;rejection[j]=F(5,6)
        check(all(F(1,8)<=u<=F(7,8) for u in rejection),'future_probe_command_in_declared_cube')
        coefficients=tuple(sum(rejection[k]*center.cells[k][i] for k in range(3)) for i in range(3))
        check(coefficients==tuple(F(1,2) if i==0 else F(1,32) if i==j else F(0) for i in range(3)),
              'future_probe_is_one_physical_failure_command')
    RESULTS['one_name_physical_collision']={'delta':delta,'rho':rho,
        'analytic_raw_error_bound':advice.max_quotient_bound,'actual_raw_error':max_error,
        'moment_name_sha256':fixed_table_digest,'physical_inputs':physical_inputs,'runs':results,
        'domain':'Complete finite two-command acquisition alphabet; eta=1/8 for admissible acquisition and future commands; N=3, T=2, four reports. Not full-cube coverage.',
        'priors':'densities 1+epsilon*(t-1/2), or uniform; all between 1/2 and 3/2.',
        'collision':'a=(0,1,2+gap), with gap=0 and both signs, one common name and no equality test.'}


def collision_lower_checks():
    rows=[]
    grid=((F(1,4),F(3,4),F(1,4)),(F(3,4),F(1,4),F(3,4)))
    for gap in (F(0),-F(1,17),F(1,17)):
        for delta in (F(1,128),F(1,1024)):
            eps=delta/2
            base=TiltedTruth(gap,0);plus=TiltedTruth(gap,eps);minus=TiltedTruth(gap,-eps)
            for t in (base,plus,minus):t.grid=grid
            for alpha in (a for d in range(4) for a in cc.formal_labels(d,3)):
                check(abs(plus.moment(alpha)-base.moment(alpha))<=delta/2 and
                      abs(minus.moment(alpha)-base.moment(alpha))<=delta/2,
                      'tilted_priors_share_slack_moment_name')
            stage_rows=[]
            for n in (1,2):
                m=3-n;slope=F(1,32)*F(1,2)**(m-1)
                integrated=F(0);variance_min=F(1);gap_min=F(1);overlap_min=F(1)
                for coded in product(tuple(product(range(2),range(4))),repeat=n):
                    h=base.actual(coded);poly=base.posterior_product(h);z=base.integral(poly)
                    def expect(shift):return base.integral({s+shift:c for s,c in poly.items()})/z
                    v=expect(2)-expect(1)**2;fmean=expect(1)-F(1,2)
                    # Probe F1 followed by constants F0; separate exponent integrals.
                    qpoly=powers_product(poly,{F(0):F(1,2)**m,F(1):slope})
                    qplus=plus.integral(qpoly)/plus.integral(poly)
                    qminus=minus.integral(qpoly)/minus.integral(poly)
                    qgap=qplus-qminus
                    check(qgap==2*eps*slope*v/(1-eps**2*fmean**2),'exact_posterior_tilt_identity_at_collision')
                    check(qgap>=2*eps*slope*v,'positive_uniform_covariance_separation')
                    wp=plus.integral(poly);wm=minus.integral(poly)
                    check(wp>=(1-eps)*z and wm>=(1-eps)*z,'history_likelihood_overlap_bound')
                    # Optimal predictor for these two history-weighted squared losses.
                    y=(wp*qplus+wm*qminus)/(wp+wm)
                    exact_half=(wp*(y-qplus)**2+wm*(y-qminus)**2)/2
                    lower=(1-eps)*z*qgap*qgap/4
                    check(exact_half>=lower,'exact_two_point_minimum_dominates_proved_bound')
                    integrated+=exact_half/F(2)**n/F(3)**m
                    variance_min=min(variance_min,v);gap_min=min(gap_min,qgap)
                    overlap_min=min(overlap_min,wp/z,wm/z)
                check(integrated>0,'positive_unconditional_floor_at_each_collision_checkpoint')
                stage_rows.append({'n':n,'m':m,'minimum_variance':variance_min,'minimum_gap':gap_min,
                                   'minimum_overlap_ratio':overlap_min,'minimum_two_model_average_risk':integrated,
                                   'risk_over_delta_squared':integrated/delta**2})
            rows.append({'gap':gap,'delta':delta,'epsilon':eps,'stages':stage_rows})
    RESULTS['sharp_collision_lower_identity']=rows


def main():
    conformance_mutations();physical_common_name();collision_lower_checks()
    result={'status':'passed','assertions':sum(COUNTS.values()),'categories':dict(COUNTS),**RESULTS,
            'scope':'Executed finite exact-rational diagnostics; no continuum enumeration or formal proof certification.'}
    out=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'validation/V13_DIAGNOSTICS.json')
    out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('status','assertions','categories','scope')},indent=2))
if __name__=='__main__':main()
