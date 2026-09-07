#!/usr/bin/env python3
"""Exact independent construction, integrated physical, and advice-floor tests.

The inherited exponent-keyed physical Truth is independent of the compiler's
formal-label arithmetic. No residual recomputed from a mutated program is an
acceptance allowance. The physical adaptive fixtures cover explicitly declared
subexperiments, not the full command cube or all asymptotic collision phases.
"""
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import certified_compiler as cc
from finite_compiler import Machine, compile_tables
from construction_contracts import inspect_construction, ContractError, bind_request


def request_for(T, commands, reports, M, bits, evaluate, predict):
    # Schema/precision are explicit fixture constants, never read from a table.
    tau=F(4,1<<bits)  # Same external error allowance as adaptive h=2^(-b).
    return bind_request(T,commands,reports,M,bits,evaluate,predict,tau/2,tau)[0]

from test_v11 import Truth, noisy_advice

COUNTS=Counter()
RESULTS={}


def check(condition,category):
    if not condition: raise AssertionError(category)
    COUNTS[category]+=1


def norm(x,y):
    return max((abs(a-b) for a,b in zip(x,y)),default=F(0))


def changed_program(p,kind):
    rows=[]; changed=0
    for n,stage in enumerate(p.transitions):
        out=[]
        for i,commands in enumerate(stage):
            targets=[]
            for u,reports in enumerate(commands):
                q=[]
                for x,j in enumerate(reports):
                    if kind=='collapse': v=0
                    elif kind=='last': v=p.state_counts[n+1]-1
                    elif kind=='erase_state': v=stage[0][u][x]
                    elif kind=='erase_command': v=commands[0][x]
                    elif kind=='erase_report': v=reports[0]
                    else: raise ValueError(kind)
                    changed+=v!=j; q.append(v)
                targets.append(tuple(q))
            out.append(tuple(targets))
        rows.append(tuple(out))
    return replace(p,transitions=tuple(rows)),changed


def physical_factory(truth,log):
    def factory(b,h):
        advice=noisy_advice(truth,b)
        alphabet=tuple(product(range(len(truth.grid)),range(4)))
        max_state=max_query=F(0)
        for n in range(3):
            for hist in product(alphabet,repeat=n):
                actual=truth.actual(hist)
                max_state=max(max_state,norm(advice.state(hist),truth.state(actual)))
                max_query=max(max_query,norm(advice.predictions(hist),truth.predictions(actual)))
        check(max_state<=h/2 and max_query<=h/2,'physical_finite_input_name_accuracy')
        check(advice.max_quotient_bound<=h/2,'physical_analytic_quotient_budget')
        log.append({'b':b,'requested_tau':h,'coefficient_moment_delta':advice.delta,
                    'actual_max_state_name_error':max_state,
                    'actual_max_query_name_error':max_query,
                    'quotient_error_certificate':advice.max_quotient_bound})
        return len(truth.grid),advice.state,advice.predictions,advice
    return factory


def exact_finite_cover_radius(points,M):
    """Exact unrestricted-centre L-infinity radius, independent of the compiler.

    A subset fits in one radius-e box iff its diameter is at most 2e.
    Thus M boxes exist iff the graph joining pairs farther than 2e is
    M-colourable. Enumerate all possible critical pair distances and decide
    colouring exhaustively (degree/saturation order is only a search heuristic).
    The physical fixtures have at most 15 distinct points, not a large solver.
    """
    points=tuple(dict.fromkeys(tuple(x) for x in points));N=len(points)
    if M>=N:return F(0)
    ds=[[norm(x,y) for y in points] for x in points]
    candidates=sorted({d/2 for row in ds for d in row})
    def feasible(radius):
        adj=[{j for j in range(N) if ds[i][j]>2*radius} for i in range(N)]
        colors=[-1]*N
        def visit(left,used):
            if not left:return True
            v=max(left,key=lambda i:(len({colors[j] for j in adj[i] if colors[j]>=0}),len(adj[i]),-i))
            forbidden={colors[j] for j in adj[v] if colors[j]>=0}
            for c in range(min(used+1,M)):
                if c in forbidden:continue
                colors[v]=c
                if visit(left-{v},max(used,c+1)):return True
            colors[v]=-1;return False
        return visit(set(range(N)),0)
    lo,hi=0,len(candidates)-1
    while lo<hi:
        mid=(lo+hi)//2
        if feasible(candidates[mid]):hi=mid
        else:lo=mid+1
    return candidates[lo]


def integrated_physical():
    receipts=[]; mutations=Counter()
    # The finite two-command experiment has genuine command and report effects.
    # Its entire alphabet and ALL histories through the synthesis horizon are
    # enumerated at every refinement. Its command approximation error is zero.
    finite_commands=((F(1,4),F(3,4),F(1,4)),
                     (F(3,4),F(1,4),F(3,4)))
    for gap,shape in ((F(0),1),(F(1,10**12),1),(F(1,7),3)):
        for domain,M in (('finite_two_command',1),('finite_two_command',2),
                         ('finite_two_command',4),('common_command_line',2)):
            truth=Truth(gap,shape)
            truth.grid=finite_commands if domain=='finite_two_command' else ((F(1,2),)*3,)
            inputs=[]; factory=physical_factory(truth,inputs)
            p,a,trace,advice=cc.adaptive_compile(2,4,M,F(0),factory,max_bits=24)
            final=trace[-1]; h=final['h']; r=final['r']
            alphabet=tuple(product(range(len(truth.grid)),range(4)))
            exact_radii=tuple(exact_finite_cover_radius(
                (truth.state(truth.actual(hist)) for hist in product(alphabet,repeat=n)),M)
                              for n in (1,2))
            exact_e=max(exact_radii)
            for t in trace:
                check(t['lower']<=exact_e<=t['upper'],'physical_exact_cover_oracle_brackets')
            check(3*r/8<=exact_e<=5*r/4,'physical_exact_cover_oracle_final_bracket')
            check(exact_e/20<h<=exact_e/3,'physical_exact_cover_oracle_selected_scale')

            cert=inspect_construction(p,a,len(truth.grid),4,M,advice.state,advice.predictions,
                request=request_for(2,len(truth.grid),4,M,final['b']+2,
                                    advice.state,advice.predictions)).require()
            check(final['radius_stop'],'physical_adaptive_radius_stop')
            check(all(not z['radius_stop'] for z in trace[:-1]),'physical_first_success')
            check(max(p.state_counts)<=M,'physical_exact_label_budget')
            check(cert.accepted,'physical_independent_contract')
            check(all(d<=v for d,v in zip(cert.max_selected_distance,cert.grid_order_limits)),
                  'physical_frozen_cover_order')
            # These allowances are fixed from the unmodified DATA, not from the
            # candidate transition table. tau=h includes all numerical rounding.
            E=[F(0)]
            for n in range(2): E.append(F(13,2)*E[-1]+cert.radii[n+1]+2*h)
            allowance=[v+h for v in E]
            max_error=F(0); paths=0
            if domain=='finite_two_command':
                words=product(tuple(product(range(2),range(4))),repeat=2)
                for hist in words:
                    m=Machine(); actual=()
                    for n,(u,x) in enumerate(hist):
                        m.step(p,n,u,x); actual+=((truth.grid[u],x),)
                        rep=truth.actual(a.representatives[n+1][m.index])
                        check(norm(truth.state(actual),truth.state(rep))<=E[n+1],
                              'physical_frozen_state_recurrence')
                        for q,value in enumerate(truth.predictions(actual)):
                            err=abs(m.output(p,n+1,q)-value);max_error=max(max_error,err)
                            check(err<=allowance[n+1],'physical_adaptive_all_queries_all_histories')
                    paths+=1
            else:
                # For g=(u,u,u), success j is u*k_j and failure is 1-u.
                # These scalar factors cancel in the posterior. Thus one command
                # code covers the whole continuous line EXACTLY. The following
                # five values are checks of the identity, not a finite-net claim.
                values=(F(1,4),F(5,17),F(1,2),F(11,17),F(3,4))
                for word in product(tuple(product(values,range(4))),repeat=2):
                    m=Machine(); actual=(); coded=()
                    for n,(u,x) in enumerate(word):
                        m.step(p,n,0,x);actual+=(((u,)*3,x),);coded+=((0,x),)
                        check(truth.state(actual)==truth.state(truth.actual(coded)),
                              'continuous_common_command_quotient_identity')
                        for q,value in enumerate(truth.predictions(actual)):
                            err=abs(m.output(p,n+1,q)-value);max_error=max(max_error,err)
                            check(err<=allowance[n+1],'physical_continuous_line_all_query_execution')
                    paths+=1
            mutation_rows={}
            for kind in ('collapse','last','erase_state','erase_command','erase_report'):
                bad,changed=changed_program(p,kind)
                if not changed:
                    mutation_rows[kind]={'changed_entries':0,'not_a_mutation':True};continue
                bad_cert=inspect_construction(bad,a,len(truth.grid),4,M,
                                              advice.state,advice.predictions,
                    request=request_for(2,len(truth.grid),4,M,final['b']+2,
                                        advice.state,advice.predictions))
                check(not bad_cert.accepted,'independent_gate_rejects_'+kind)
                check(bad_cert.grid_order_limits==cert.grid_order_limits,
                      'mutation_cannot_enlarge_reference_allowance')
                check(any(v[0]=='nearest_transition' for v in bad_cert.violations),
                      'mutated_nearest_transition_detected')
                mutation_rows[kind]={'changed_entries':changed,
                                    'violations':len(bad_cert.violations),'accepted':False}
                mutations[kind]+=changed
            trans_bits=(M).bit_length()
            receipts.append({'gap':gap,'prior_shape':shape,'domain':domain,'M':M,
                'horizon':2,'formal_total_trial_budget':3,'command_count':len(truth.grid),
                'domain_description':str(truth.grid) if domain=='finite_two_command'
                    else 'g=(u,u,u), 1/4<=u<=3/4; exact posterior quotient, not the full cube',
                'coverage':'all alphabet histories' if domain=='finite_two_command'
                    else 'analytic exact command quotient; five-value trajectory checks',
                'paths_executed':paths,'state_counts':p.state_counts,
                'transition_entries':cert.transition_entries,'output_entries':cert.output_entries,
                'table_payload_bits':cert.transition_entries*trans_bits+
                                      cert.output_entries*(p.output_bits+1),
                'payload_excludes':'fixed interface, clock, framing, offline histories and workspace',
                'output_bits':p.output_bits,'input_trace':inputs,'stopping_trace':trace,
                'radii':cert.radii,'exact_true_stage_cover_radii':exact_radii,
                'exact_true_cover_radius':exact_e,'cover_bracket':(3*r/8,5*r/4),
                'max_actual_query_error':max_error,'frozen_query_bounds':allowance,
                'contract_checks':cert.checks,'mutations':mutation_rows})
    for kind in ('collapse','erase_state','erase_command','erase_report'):
        check(mutations[kind]>0,'nonvacuous_'+kind+'_coverage')
    RESULTS['integrated_physical']=receipts
    RESULTS['physical_mutated_entries_rejected']=dict(mutations)


def interval_order():
    rows=[]
    for M in (1,2,4,8,16,32):
        grid=tuple(F(1,4)+F(j,16*M) for j in range(8*M+1))
        def state(hist):
            s=F(1,2)
            for u,x in hist:s=(s+grid[u])/2
            return (s,)
        p,a=compile_tables(1,len(grid),1,M,12,state,state)
        cert=inspect_construction(p,a,len(grid),1,M,state,state,
                request=request_for(1,len(grid),1,M,12,state,state)).require()
        e=F(1,8*M)
        maximum=F(0)
        for u in range(len(grid)):
            m=Machine();m.step(p,0,u,0)
            maximum=max(maximum,abs(m.output(p,1,0)-state(((u,0),))[0]))
        check(maximum<=2*e,'interval_covering_order_fixed_optimal_radius')
        check(cert.radii[1]<=2*e,'interval_frozen_radius_order')
        bad,changed=changed_program(p,'collapse')
        cert_bad=inspect_construction(bad,a,len(grid),1,M,state,state,
                request=request_for(1,len(grid),1,M,12,state,state))
        m=Machine();m.step(bad,0,len(grid)-1,0)
        collapsed=abs(m.output(bad,1,0)-F(5,8))
        check(collapsed==F(1,4),'collapsed_interval_error_exact')
        check(collapsed/e==2*M,'collapsed_interval_unbounded_order_ratio')
        if M>1:check(not cert_bad.accepted,'interval_collapse_independently_rejected')
        rows.append({'M':M,'command_mesh':F(1,32*M),'true_e':e,
                     'correct_max_grid_error':maximum,'correct_radius':cert.radii[1],
                     'collapsed_error':collapsed,'collapsed_over_optimal':collapsed/e,
                     'changed':changed,'contract_violations':len(cert_bad.violations)})
    RESULTS['interval_covering_order']=rows
    # Compiling the same input through a corrupted call site must fail BEFORE
    # the adaptive routine returns any certificate/program.
    original=cc.compile_tables
    def collapse(*args,**kwargs):
        p,a=original(*args,**kwargs)
        return changed_program(p,'collapse')[0],a
    cc.compile_tables=collapse
    def factory(b,h):
        grid=(F(1,4),F(1,2),F(3,4))
        def state(hist):
            return (F(1,2),) if not hist else ((F(1,2)+grid[hist[0][0]])/2,)
        return 3,state,state,None
    try:
        try:
            cc.adaptive_compile(1,1,2,F(0),factory)
        except ContractError:
            check(True,'adaptive_call_site_collapse_rejected')
        else:raise AssertionError('mutated adaptive compiler returned')
    finally:cc.compile_tables=original
    # All coordinates identical: a different target is still an incorrect tie.
    p,a=compile_tables(1,2,1,2,4,lambda h:(F(1,2),),lambda h:(F(1,2),))
    bad=replace(p,transitions=((( (1,), (1,) ),),))
    fixed=lambda h:(F(1,2),)
    c=inspect_construction(bad,a,2,1,2,fixed,fixed,
                           request=request_for(1,2,1,2,4,fixed,fixed))
    check(not c.accepted and all(v[0]=='nearest_transition' for v in c.violations),
          'fixed_tie_rule_independently_enforced')


def robust_floor_tests():
    rows=[]
    for M,rho in ((1,F(1,1024)),(2,F(1,32)),(4,F(1,16)),(4,F(1,4))):
        def factory(b,h,tau):
            segments=max(1,1<<max(0,b-2))
            grid=tuple(F(1,4)+F(j,2*segments) for j in range(segments+1))
            def state(hist):
                return (F(1,2),) if not hist else ((F(1,2)+grid[hist[0][0]])/2,)
            return len(grid),state,state,grid
        p,a,trace,grid=cc.robust_adaptive_compile(1,1,M,F(1,2),factory,rho,
                                                 max_candidates=200000)
        e=F(1,8*M);last=trace[-1];c=F(9,2)
        for t in trace:
            check(t['lower']<=e<=t['upper'],'common_advice_bracket_both_models')
        check(last['h']>(e+rho)/(10*c+2) and last['h']<=e+rho,
              'common_advice_first_success_scale')
        fixed=lambda hist:(F(1,2),) if not hist else ((F(1,2)+grid[hist[0][0]])/2,)
        cert=inspect_construction(p,a,len(grid),1,M,fixed,fixed,
              request=request_for(1,len(grid),1,M,last['b']+2,fixed,fixed)).require()
        # Two genuinely different systems: state=true_base +/-rho/4 at ALL
        # stages, transition T(s,u)=(s+u)/2 +/-rho/8, same input name.
        bound=last['h']/2+cert.radii[1]+3*last['tau']
        for sign in (-1,1):
            for k in range(65):
                u=F(1,4)+F(k,128)
                code=min(range(len(grid)),key=lambda j:(abs(grid[j]-u),j))
                m=Machine();m.step(p,0,code,0)
                truth=(F(1,2)+u)/2+sign*rho/4
                check(abs(m.output(p,1,0)-truth)<=bound,'one_program_two_models_offgrid')
        rows.append({'M':M,'rho':rho,'true_e_both_models':e,'trace':trace,
                     'common_program_query_bound':bound})
    RESULTS['common_advice_robust_realization']=rows
    # The explicit positive detector lower witness has a common finite input
    # name but different physical predictions after the same accepted cell.
    witness=[]
    for delta in (F(1,128),F(1,256),F(1,1024)):
        eps=6*delta
        def moment(k,sign):return F(1,k+1)+sign*eps*F(k,(k+1)*(k+2))
        for k in range(13):
            for sign in (-1,1):
                check(abs(moment(k,sign)-F(1,k+1))<=delta,'common_moment_name_compatible')
        qs=tuple(F(1,2)+moment(1,sgn)/32 for sgn in (-1,1))
        gap=qs[1]-qs[0]
        check(gap==delta/16,'positive_detector_advice_floor_gap')
        check((gap/2)**2==delta**2/1024,'positive_detector_two_point_squared_floor')
        witness.append({'delta':delta,'density_tilt':eps,'predictions':qs,
                        'conditional_minimax_squared_floor':(gap/2)**2,
                        'unconditional_event_mass_lower':F(1,16)})
    RESULTS['positive_detector_advice_floor_witness']=witness
    # Small changes in calibration move reachable sets, without comparing or
    # removing coincident formal labels. This is a finite, paired-history check.
    a=Truth(F(0),1); b=Truth(F(1,10**6),1)
    commands=((F(1,4),F(3,4),F(1,4)),(F(3,4),F(1,4),F(3,4)))
    a.grid=b.grid=commands
    delta=max(abs(a.moment(alpha)-b.moment(alpha))
              for n in range(4) for alpha in cc.formal_labels(n,3))
    for n in (1,2):
        D=(F(3)**n) # exact coefficients coincide, only moment error is present
        for hist in product(tuple(product(range(2),range(4))),repeat=n):
            check(norm(a.state(a.actual(hist)),b.state(b.actual(hist)))<=2*D*32**n*delta,
                  'paired_physical_history_moment_stability')


def bit_tests():
    rows=[]
    for b in (3,8,17,32):
        for N in (2,3,5,9):
            x=F((1<<b)-1,1<<b);power=x**N
            check(power.denominator==1<<(N*b),'exact_rational_denominator_Nb')
            check(power.denominator.bit_length()-1==N*b,'exact_rational_not_additive')
            rows.append({'b':b,'N':N,'exact_fractional_bits':N*b})
    RESULTS['exact_rational_bit_lengths']=rows


def main():
    integrated_physical();interval_order();robust_floor_tests();bit_tests()
    out={'passed':True,'assertions':sum(COUNTS.values()),'categories':dict(COUNTS),
         'measurements':RESULTS,'scope':'finite diagnostics, not a proof or all-phase/full-cube validation'}
    text=json.dumps(out,indent=2,default=lambda x:str(x) if isinstance(x,F) else x)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(text)
    print(json.dumps({'passed':True,'assertions':sum(COUNTS.values()),'categories':dict(COUNTS)},indent=2))
if __name__=='__main__':main()
