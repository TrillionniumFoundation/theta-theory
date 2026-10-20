#!/usr/bin/env python3
"""Auxiliary exact arithmetic and real first-hit diagnostics, NOT proof certification."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(s, a): return (s * a[0], s * a[1])
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def perp(a): return (-a[1], a[0])
def norm(a): return math.hypot(a[0], a[1])
def unit(a):
    r = norm(a)
    require(r > 0, 'zero vector')
    return mul(1 / r, a)
def rational_unit(t): return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def exact_checks() -> dict[str, Any]:
    R, ca, H, N = F(47, 100), F(1, 416640), F(28, 5), 94
    T = H + 4 * R
    inequalities = {
        'anchor': F(443)**2 - R/ca,
        'flight': F(38)**2 - 2*N*T,
        'turning': F(14)**2 - 4*N*R,
        'quarter': F(22)**2 - 2*R*(443+38+14+1),
        'endpoint': F(4) - 8*R,
        'longitudinal': H*H - F(3847, 124),
        '94_flights': 94*F(3,50) - H,
    }
    for name, gap in inequalities.items():
        require(gap > 0, 'constant inequality: '+name)
    require(T == F(187,25), 'comparison flight bound')
    require(F(1,4480)/93 == ca, 'anchor denominator')
    require(2*H*F(1,4480) == F(1,400), 'turning buffer')
    widths = [F(961,4804), F(13697401,73866304), F(529,3136), F(75,448)]
    require(all(w < F(179,400)**2 for w in widths), 'whole-interval buffer table')
    # Exact reconstruction of the four rational squared widths from the formulas.
    t = F(1,60)
    require(F(3,16)*(1+2*t)**2/(1+3*t*t) == widths[0], 'horizontal endpoint')
    for (a,t), expected in zip([(5,F(1,60)),(2,F(1,12)),(1,F(1,5))], widths[1:]):
        s, nn = 2*a+1, a*a+a+1
        brace = F(s,2*nn)+F(3,2*nn)*t+abs(s*t-1)
        require(F(3,16)*brace*brace/(1+3*t*t) == expected, 'row endpoint')
    disk_cases = 0
    for r in (F(9,20), F(23,50), F(47,100)):
        for t in (F(-1,3), F(0), F(1,5), F(2,3)):
            n = rational_unit(t)
            require(dot(n,n) == 1, 'rational unit length')
            for u in (F(0), F(1,3), F(1)):
                z = mul(r*u, rational_unit(t+F(1,7)))
                delta = sub(z,mul(r,n))
                lhs = 2*r*(r-dot(n,z))-dot(delta,delta)
                require(lhs == r*r-dot(z,z) and lhs >= 0, 'disk curvature identity')
                disk_cases += 1
    transverse_cases, omitted_turn_detected = 0, False
    # These arbitrary vector arrays test algebra, not physical realizability.
    for m in (1,2,3,8,13,94):
        v = [rational_unit(F((i%5)-2,7)) for i in range(m)]
        vh = [rational_unit(F((2*i%7)-3,11)) for i in range(m)]
        ell = [F(4+(i%4),5) for i in range(m)]
        tau = [F(3+(i%3),4) for i in range(m)]
        delta = [(F(2,7),F(-1,9))]
        rr = []
        for i in range(m):
            rvec = mul(ell[i],sub(vh[i],v[i])); rr.append(rvec)
            delta.append(add(delta[-1],add(mul(ell[i]-tau[i],v[i]),rvec)))
        for i in range(1,m+1):
            for j in set((0,i-1,i//2)):
                if j >= i: continue
                left = dot(perp(v[i-1]),delta[i])
                base = dot(perp(v[j]),delta[j])
                flights = sum((dot(perp(v[l]),rr[l]) for l in range(j,i)), F(0))
                turn = sum((dot(sub(perp(v[l]),perp(v[l-1])),delta[l]) for l in range(j+1,i)), F(0))
                require(left == base+flights+turn, 'exact transverse identity')
                omitted_turn_detected |= (left != base+flights)
                transverse_cases += 1
    require(omitted_turn_detected, 'missing turning term negative control did not fire')
    anchor_cases = 0
    # Conditional combinatorial anchor arrays; these are NOT billiard samples.
    for m in (1,2,93,94,95,188,257,1001):
        anchors = {i for i in range(1,m) if i%93 == 1}
        for i in range(1,m):
            if i in anchors: continue
            j = max([0]+[a for a in anchors if a < i])
            require(i-j < 94, 'anchor distance boundary')
            anchor_cases += 1
    # A continuum family of genuine one-flight records has exact rational members.
    # Their written all-center proof is separate; these members are diagnostics.
    actual_exact = []
    guard_pass, guard_fail = 0, 0
    for r in (F(9,20), F(23,50), F(47,100)):
        for t in (F(0),F(1,100000000),F(1,10000),F(-1,10000),F(1,20)):
            c,s = rational_unit(t)
            E = 2*r*(1-c)
            delta2 = 2*r*r*(1-c)
            require(delta2 == r*E, 'one-flight endpoint identity')
            require(delta2*delta2 <= F(22)**4*E, 'one-flight quarter inequality')
            # Off-axis lattice rows are >=sqrt(3)/2 > 4/5 away from y=0.
            g = F(4,5)-abs(r*s)-r
            require(g > 0 and 1-2*r*c > 0, 'one-flight physical clearance')
            passes = g**4 > F(22)**4*E
            guard_pass += int(passes); guard_fail += int(not passes)
            actual_exact.append({'R':str(r),'parameter':str(t),'E':str(E),'delta_squared':str(delta2),'clearance_lower_bound':str(g),'sufficient_guard_passes':passes,'minimum_is_physical':True})
    require(guard_pass > 0 and guard_fail > 0, 'sufficient-not-necessary guard controls')
    bounce_lengths = [1,2,93,94,188,257]
    for m in bounce_lengths:
        require(2+2*(m-1) == 2*m, 'normal bounce endpoint accounting')
    return {'constant_gaps':{k:str(v) for k,v in inequalities.items()},'buffer_widths_squared':[str(w) for w in widths],
            'disk_cases':disk_cases,'transverse_identity_cases':transverse_cases,'missing_turning_term_negative_control':omitted_turn_detected,
            'conditional_anchor_index_cases':anchor_cases,'actual_exact_one_flight_cases':actual_exact,'guard_passes':guard_pass,'guard_failures_retained':guard_fail,
            'normal_bounce_flight_counts':bounce_lengths,'scope':'exact finite arithmetic and explicitly identified actual one-flight/bounce families; not continuum proof certification'}


def lattice(a: int,b: int): return (a+b/2, math.sqrt(3)*b/2)


def next_hit(q, v, current, R):
    ac = round(q[0]-q[1]/math.sqrt(3)); bc = round(2*q[1]/math.sqrt(3))
    hits = []
    for a in range(ac-9,ac+10):
        for b in range(bc-9,bc+10):
            if (a,b) == current: continue
            o = lattice(a,b); d = sub(q,o); along = dot(d,v)
            discriminant = along*along-dot(d,d)+R*R
            if discriminant <= 0: continue
            t = -along-math.sqrt(discriminant)
            if t > 1e-9: hits.append((t,a,b,o))
    require(bool(hits), 'no first-hit candidate in enclosing lattice rectangle')
    t,a,b,o = min(hits)
    require(t <= 28/5+1e-8, 'sample violates horizon')
    hit = add(q,mul(t,v)); normal = unit(sub(hit,o))
    require(dot(v,normal) < -1e-10, 'singular or numerically unresolved hit; not silently skipped')
    hit = add(o,mul(R,normal))
    return hit, normal, (a,b), o


def trace_record(R: float,alpha: float,phi: float,m: int) -> dict[str,Any]:
    q = (R*math.cos(alpha),R*math.sin(alpha))
    v = (math.cos(alpha+phi),math.sin(alpha+phi))
    require(dot(q,v) > 0, 'initial exterior direction')
    current=(0,0); points=[q]; centers=[(0.0,0.0)]; ids=[current]
    for _ in range(m):
        q,n,current,o = next_hit(q,v,current,R)
        points.append(q); centers.append(o); ids.append(current)
        v = unit(sub(v,mul(2*dot(v,n),n)))
    tau = [norm(sub(points[i+1],points[i])) for i in range(m)]
    vv = [unit(sub(points[i+1],points[i])) for i in range(m)]
    normals = [mul(1/R,sub(q,o)) for q,o in zip(points,centers)]
    cc = [dot(vv[0],normals[0])]+[-dot(vv[i-1],normals[i]) for i in range(1,m)]+[-dot(vv[-1],normals[-1])]
    require(all(c > 0 for c in cc), 'nonregular sample')
    require(min(tau) >= 3/50-1e-8, 'sample flight lower bound')
    for i in range(1,m):
        require(norm(sub(sub(vv[i],vv[i-1]),mul(2*cc[i],normals[i]))) < 1e-8, 'sample reflection residual')
    blocks = [sum(cc[a+1:a+94]) for a in range(m-93)]
    require(all(x >= 1/4480-1e-8 for x in blocks), 'sample anchor block')
    E = R*(2-cc[0]-cc[-1]); L=sum(tau)
    require(E >= -1e-12 and E <= 2*R+1e-12, 'sample endpoint defect range')
    E=max(E,0.0)
    # Explicit feasible sublevel configuration, not asserted to be a minimum.
    Y=list(points)
    Y[0]=add(centers[0],mul(R,unit(sub(points[1],centers[0]))))
    Y[-1]=add(centers[-1],mul(R,unit(sub(points[-2],centers[-1]))))
    ell=[norm(sub(Y[i+1],Y[i])) for i in range(m)]
    vh=[unit(sub(Y[i+1],Y[i])) for i in range(m)]
    dd=[mul(-1,vv[0])]+[sub(vv[i-1],vv[i]) for i in range(1,m)]+[vv[-1]]
    D=sum(dot(d,o)-R*norm(d) for d,o in zip(dd,centers))
    flight=sum(ell[i]*norm(sub(vh[i],vv[i]))**2/2 for i in range(m))
    contact=sum(dot(dd[i],sub(Y[i],centers[i]))+R*norm(dd[i]) for i in range(m+1))
    displacement=[norm(sub(y,q)) for y,q in zip(Y,points)]
    tolerance=1e-8*max(1,L)
    require(sum(ell) <= L+tolerance, 'not actually in sublevel')
    require(abs((sum(ell)-D)-(flight+contact)) <= tolerance, 'sample gap identity')
    require(abs(L-D-E) <= tolerance, 'sample endpoint normalization')
    require(flight >= -tolerance and contact >= -tolerance and flight+contact <= E+tolerance, 'sample positive budget')
    require(sum(cc[i]*displacement[i]**2 for i in range(1,m)) <= R*E+tolerance, 'sample contact budget')
    require(max(displacement) <= 22*E**0.25+1e-7, 'sample localization')
    return {'R':R,'alpha':alpha,'phi':phi,'flights':m,'points':points,'lattice_centers':ids,
            'incidence_cosines':cc,'flight_lengths':tau,'endpoint_defect':E,'true_roof':L,'sublevel_roof':sum(ell),
            'max_sublevel_displacement':max(displacement),'gap_residual':abs((sum(ell)-D)-(flight+contact)),
            'block_count':len(blocks),'minimum_94_flight_incidence_sum':min(blocks),'status':'passed',
            'scope':'floating-point genuine first-hit diagnostic; no certified continuous geometry or solver minimum'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result={'status':'started','exact':exact_checks(),'real_records':[],
            'continuum_proof_certificate':False,'full_raw_pointwise_LLT_proved':False,'four_coordinate_inversion_completed':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    try:
        for R in (0.45,0.46,0.47):
            for alpha,phi in ((0.12,0.17),(0.41,-0.23),(0.90,0.31),(1.31,-0.11)):
                result['real_records'].append(trace_record(R,alpha,phi,192))
        result['status']='all_explicit_diagnostics_passed'
    except Exception as exc:
        result['status']='failed';result['error']=repr(exc)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        raise
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'exact_transverse_cases':result['exact']['transverse_identity_cases'],
                      'actual_records':len(result['real_records']),'actual_flights':sum(r['flights'] for r in result['real_records']),
                      'all_overlapping_94_flight_blocks':sum(r['block_count'] for r in result['real_records']),
                      'formal_proof_certificate':False},sort_keys=True))

if __name__ == '__main__':
    main()
