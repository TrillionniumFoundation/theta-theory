#!/usr/bin/env python3
"""Independent finite controls for the A2 v67 review.
No author checker is imported. These controls do not certify an infinite-dimensional
inverse, global billiard realization, trace-class limit, or statistical theorem.
Requires Python 3 and SymPy. All logical checks also execute under python -O.
"""
from fractions import Fraction as F
import json
import sympy as sp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vmax(v):
    return max(abs(x) for x in v)


def distance(v, w):
    return vmax([a-b for a, b in zip(v, w)])


def datum(r, seed):
    k=[F(4+(i+seed)%4,4) for i in range(r)]
    a=[F(2+(2*i+seed)%3,12) for i in range(r)]
    c=[(k[i-1]/a[i-1]-k[i-1]-k[i]+k[i]*a[i])/2 for i in range(r)]
    s=[c[i]+k[i]*(1-a[i]) for i in range(r)]
    require(min(c)>0 and min(s)>0, 'Nonpositive constructed quadratic datum')
    require(all(a[i]==k[i]/(k[i]+c[(i+1)%r]+s[(i+1)%r]) for i in range(r)), 'Schur identity')
    return k,a,c,s


def phi(k,s,z):
    r=len(k)
    return [max(F(0),s[i]-k[i]+k[i]**2/(k[i]+s[(i+1)%r]+z[(i+1)%r])) for i in range(r)]


def contraction_controls():
    counts={'quadratic_data_sets':0,'a_priori_bounds':0,'residual_bounds':0,
            'inexact_evaluation_bounds':0,'positive_image_certificates':0,'two_point_bounds':0}
    data=[]
    for r in range(2,8):
        for seed in range(5):
            k,a,c,s=datum(r,seed);data.append((k,a,c,s));counts['quadratic_data_sets']+=1
            q=max((k[i]/(k[i]+s[(i+1)%r]))**2 for i in range(r))
            for start in [[F(0)]*r,[2*x for x in c],[x+F(1,7) for x in c]]:
                v=start[:];initial=distance(phi(k,s,v),v)
                for m in range(10):
                    w=phi(k,s,v);err=distance(v,c);E=distance(w,v)/(1-q)
                    require(err<=q**m*initial/(1-q),'First-increment bound')
                    require(err<=E,'Residual bound')
                    counts['a_priori_bounds']+=1;counts['residual_bounds']+=1
                    eta=F(1,1000*(m+1))
                    inexact=[w[i]+(-1)**i*eta for i in range(r)]
                    require(err<=(distance(inexact,v)+eta)/(1-q),'Inexact evaluation certificate')
                    counts['inexact_evaluation_bounds']+=1
                    if min(v)>E:
                        require(min(c)>0,'False positive membership certificate')
                        counts['positive_image_certificates']+=1
                    v=w
            # Perturb the action data, then certify a two-point estimate by a rational
            # approximate fixed point with its own rigorous residual error.
            ss=[s[i]+F(i+1,200) for i in range(r)]
            qq=max((k[i]/(k[i]+min(s[(i+1)%r],ss[(i+1)%r])))**2 for i in range(r))
            z=c[:]
            for _ in range(25): z=phi(k,ss,z)
            tail=distance(phi(k,ss,z),z)/(1-qq)
            bound=(1+qq)/(1-qq)*distance(s,ss)
            require(distance(z,c)+tail<=bound,'Two-point bound with residual enclosure')
            counts['two_point_bounds']+=1
    nonimage=phi([F(1),F(1)],[F(1,10),F(10)],[F(0),F(109,11)])
    require(nonimage==[F(0),F(109,11)],'Nonimage control')
    k=[F(1)]*2;s=[F(3,4)]*2
    v1=phi(k,s,[F(0)]*2);v2=phi(k,s,v1)
    require(v2[0]<F(1,4)<v1[0], 'Nonmonotone iteration control')
    counts['nonimage_fixed_point']=[str(x) for x in nonimage]
    counts['nonmonotone_first_two_iterates']=[str(v1[0]),str(v2[0])]
    return counts,data


def row_norm(M):
    return max(sum(abs(M[i,j]) for j in range(M.cols)) for i in range(M.rows))


def signed_matrix_controls(data):
    counts={'signed_block_pairs':0,'directional_resolvent_identities':0,
            'derivative_norm_bounds':0,'two_point_block_bounds':0,
            'incorrect_commuted_derivative_detected':0}
    for k,a,c,s in data:
        r=len(k)
        if r>5: continue
        direction=sp.Matrix([(-1)**i*sp.Rational(i+1,r) for i in range(r)])
        alpha=max(k[i]/(k[i]+s[(i+1)%r]+c[(i+1)%r]/2) for i in range(r))
        ds=max(k[i]/(k[i]+s[(i+1)%r]+c[(i+1)%r]/2)**2 for i in range(r))
        for n in [3,4,5]:
            def matrices(v):
                sig=[(-1)**(i+1)*k[i]/(k[i]+s[(i+1)%r]+v[(i+1)%r]) for i in range(r)]
                T=sp.zeros(r)
                for i in range(r): T[i,(i+1)%r]=sp.Rational(sig[i])**n
                B=(sp.eye(r)+T).inv()
                return sig,T,B,2*B-sp.eye(r)
            sig,T,B,D=matrices(c)
            vv=[c[i]+F(i+1,1000*r) for i in range(r)]
            _,_,_,DD=matrices(vv)
            dT=sp.zeros(r)
            for i in range(r):
                j=(i+1)%r
                deriv=-(-1)**(i+1)*sp.Rational(k[i])/(sp.Rational(k[i]+s[j]+c[j])**2)
                dT[i,j]=n*sp.Rational(sig[i])**(n-1)*deriv*direction[j]
            derivative=-2*B*dT*B
            require((sp.eye(r)+T)*derivative+dT*(D+sp.eye(r))==sp.zeros(r), 'Noncommutative derivative identity')
            b=sp.Rational((1+alpha**n)/(1-alpha**n))
            beta=sp.Rational(2*n*alpha**(n-1)*ds/(1-alpha**n)**2)
            require(row_norm(D)<=b,'Signed inverse block norm')
            require(row_norm(derivative)<=beta*max(abs(x) for x in direction), 'Derivative norm')
            require(row_norm(DD-D)<=beta*sp.Rational(distance(vv,c)), 'Two-point block Lipschitz bound')
            if derivative != -2*B*B*dT: counts['incorrect_commuted_derivative_detected']+=1
            for key in ['signed_block_pairs','directional_resolvent_identities','derivative_norm_bounds','two_point_block_bounds']:
                counts[key]+=1
    return counts


def cubic_propagation_control():
    c=F(1,4);s=F(3,4);q=F(16,49);v=F(9,28);a=F(1,2)
    observed_a=1/(1+s+v);s3=F(90,7)
    reconstructed=(1-observed_a**3)/(1+observed_a**3)*s3
    error=abs(reconstructed-10)
    prior=q/(1-q)*v
    next_v=max(F(0),s-1+1/(1+s+v))
    residual=abs(next_v-v)/(1-q)
    L3=F(2160,343)  # alpha=1/2, d_*=1/4, U3=90/7, R3=0 on normal pairs.
    require(error==F(48740,189931) and error>prior,'Old coefficient-one negative control')
    require(error<=L3*abs(v-c)<=L3*residual,'Corrected cubic propagation')
    return {k:str(x) for k,x in {'c':c,'s':s,'iterate':v,'observed_ratio':observed_a,
        'cubic_error':error,'first_increment_bound':prior,'residual_bound':residual,
        'sufficient_L3':L3,'L3_times_actual_curvature_error':L3*abs(v-c)}.items()}


def leading_information_control():
    x,s,z=sp.symbols('x s z',real=True)
    # Exactly integrate the trigonometric-polynomial support-area expression by
    # moments int sin^(2j) = 2*pi*binomial(2j,j)/4^j.
    I=lambda j: 2*sp.pi*sp.binomial(2*j,j)/4**j
    area=sp.pi+s*I(2)+z*I(3)+s*s*(17*I(4)-16*I(3))/2+s*z*(25*I(5)-24*I(4))+z*z*(37*I(6)-36*I(5))/2
    zp=-sp.diff(area,s).subs({s:0,z:0})/sp.diff(area,z).subs({s:0,z:0})
    require(zp==-sp.Rational(6,5),'Area-preserving tangent')
    h=1+s*sp.sin(x)**4+z*sp.sin(x)**6
    rho=h+sp.diff(h,x,2)
    rho0=sp.simplify(rho.subs(x,0));rho2=sp.simplify(sp.diff(rho,x,2).subs(x,0))
    require(rho0==1 and rho2==24*s,'Contact curvature and fourth derivative')
    graph_q=sp.simplify((3*rho0-rho2)/rho0**4)
    # At g=kappa=1: cosh(2gamma)=7, sinh(2gamma)=4sqrt(3), a=sqrt(3).
    derivative=sp.simplify(-sp.Rational(9,1)/(12*3*4*sp.sqrt(3))*sp.diff(graph_q,s))
    require(derivative==sp.sqrt(3)/2,'Nonlinear coefficient response')
    return {'support_area':str(sp.expand(area)),'area_preserving_z_prime':str(zp),
            'fourth_graph_derivative':str(graph_q),'nonlinear_response':str(derivative),
            'scope':'Exact support and local coefficient identities, not equal marked length spectra.'}


if __name__=='__main__':
    c,data=contraction_controls()
    out={'scope':'Finite algebra and the stated local smooth/support controls only; no author code imported.',
         'contraction':c,'signed_matrix':signed_matrix_controls(data),
         'cubic_propagation':cubic_propagation_control(),'leading_information':leading_information_control()}
    print(json.dumps(out,indent=2,sort_keys=True))
