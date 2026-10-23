# Candidate proof: sharp square-root sensitivity at two counted labels

This is new author-side mathematics, not an independent review. Baseline: General Theta Foundations I R79 source 90cae2f5aca243b39d3a2194a4d6e0696671a101 (publication a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2), sections 54–56. Please challenge all steps, especially global minimizers at eta=0 and the compactness argument. No numerical calculation is a premise.

## Primitive family and claim

Two fixed scalar hidden models, commands a,b, one nonterminal report, unit cost, mandatory success stopping, pure initial label 1. In model 0, success probabilities are (1-eta,0); in model 1 they are (0,1/2). Eta is in [0,1/4]. Let V_2(eta) be the robust expected-call optimum over all stochastic two-label controllers. Primitive Hausdorff discrepancy from eta=0 is exactly eta; a uniform independent fair-command one-label fallback has cost at most 4.

Put L=(1+sqrt(17))/2, r0=1/L. Claim: V_2(0)=L. Every optimal controller has command-a probabilities r=r0 at the prescribed initial label and s=0 at label 2; after an a failure it goes from 1 to 2, after b failure it stays at 1, and all b failures at 2 stay at 2. The transition after a failure at label 2 is arbitrary because a has probability zero there. Thus its second label is unreachable and dark under model 0, but recurrent before success under model 1. For some eta0>0, all 0<eta<eta0 obey sqrt(eta)/100 <= V_2(eta)-L <= 4 sqrt(eta). Therefore the R79 uniform square-root exponent is optimal, even at fixed physical dimension 1, two models, two commands and M=2. This is a worst-class exponent statement, not a claim about every experiment or every memory budget.

## Exact controller coordinates

Let r,s be the probabilities of a in labels 1,2. Let xa,xb be probabilities of moving 1->2 following a,b failure; ya,yb probabilities of moving 2->1 following a,b failure. These six parameters range independently over [0,1]. Under a scalar model with command success probabilities pa,pb, put
u=pa*r+pb*(1-r), v=pa*s+pb*(1-s),
alpha=(1-pa)*r*xa+(1-pb)*(1-r)*xb,
beta=(1-pa)*s*ya+(1-pb)*(1-s)*yb.
When the full two-label failure matrix is transient, the initial expected cost is
C=(v+alpha+beta)/(u*v+u*beta+v*alpha),
and the other-label cost is (u+alpha+beta)/(same denominator). Thus the sign of W1-W2 equals the sign of v-u. If label 2 is inaccessible, alpha=0 and the initial cost is 1/u, even if its own denominator is zero. In all cases of finite initial cost, the polynomial inequality
v+alpha+beta <= b*(u*v+u*beta+v*alpha)
is necessary for C<=b; when numerator and denominator both vanish it is the harmless inequality 0<=0, and the separate maximal-success bound remains valid.

## The noiseless global lower bound and rigidity: r>=s

Assume both model costs <=L. The conditional success cap gives r>=1/L and s<=h:=1-2/L. Set t=(1-r)xb, z=(1-s)yb. At eta=0, changing xa to 1 and ya to 0 does not affect model 0 and can only improve model 1: model 1 prefers the smaller-a row. The zero-cost edge cases can be checked directly; alternatively use monotone finite-horizon control with those two rows. The resulting model-1 necessary budget inequality, multiplied by 4, is
E=2+4r-2s-L(1-s)(1+r)+[2-L(1-s)]t+[2-L(1-r)]z <=0.
The model-0 polynomial budget inequality gives
(1-Ls)t <= (Lr-1)(s+z).
Since s<=h<1/L, the first factor is positive and 2-L(1-s)<=0. Consequently
P_L(r,s,z):=[2+4r-2s-L(1-s)(1+r)](1-Ls)
 +[2-L(1-s)](Lr-1)(s+z)+[2-L(1-r)]z(1-Ls) <=0.
Use L^2=L+4. P_L is affine in r, with derivative
4-L-Ls+L(3-L)z >0
on r>=1/L, 0<=s<=h, z>=0. At r=1/L,
P_L(1/L,s,z)=[(L-1)s+(3-L)z](1-Ls).
It follows P_L>=0, with equality only r=1/L,s=z=0. Then t=0. The actual model-1 cost is strictly larger than L unless xa=1. This establishes the stated unique structure for r>=s.

## Excluding the opposite row order r<=s

Suppose again both costs <=L. Success caps give 0<=r<=h and s>=1/L. At eta=0, improving model 1 sets xa=0,ya=1. With t,z as above its necessary inequality is
E=2(1+s+t+z)-L[(1-r)(1+s+z)+(1-s)t] <=0.
The model-0 inequality forces s>1/L and
 t >= (1-Lr)(s+z)/(Ls-1).
The coefficient 2-L(1-s) of t in E is positive. Substituting the lower bound and multiplying by Ls-1 yields
P_low=Q(r,s)+(2L-4)(s-r)z <=0,
Q=(2L-4)s^2+(L-4)s+L-2+r[(8-L)s-L].
But Q is affine in r. At r=0 its leading coefficient is positive and its discriminant is 17L-44<0, so Q>0. At r=h it is
s[(2L-4)s+10-4L],
which is positive for s>=1/L since the bracket at 1/L is 13-5L>0. Therefore Q>0 throughout 0<=r<=h, contradiction. Equality r=s cannot be optimal either. The endpoint inequalities also rule out missing zero-denominator cases.

## Attainment at eta=0

Use r=r0,s=0,xa=1,xb=yb=0. Model 0 never reaches label 2 and costs 1/r0=L. Model 1 costs (2+4r0)/(1+r0)=L because 4r0^2+r0-1=0. This proves both global optimum and rigidity without numerical optimization.

## An explicit upper bound for eta>0

Keep those rows and xa,xb; set yb=epsilon and ya=0. The exact costs are
C0=L/(1-eta)+eta/[(1-eta)epsilon],
C1=(2+4r0+2epsilon)/[1+r0+(1-r0)epsilon].
Thus C1-L=(3-L)epsilon/[1+r0+(1-r0)epsilon] <=epsilon.
Choose epsilon=sqrt(eta). For eta<=1/4, C0-L=(L eta+sqrt(eta))/(1-eta) <=4 sqrt(eta), proving the upper bound. All states are counted; this is a label update, not a physical reset or a clock.

## Compactness and local coordinates

For every eta>=0 the controller parameter cube is compact, and each model's infinite expected cost is the supremum of continuous nonnegative finite partial sums. Therefore the robust cost is jointly lower semicontinuous in (eta,gamma), and an optimizer exists when the fallback gives a finite cap. In addition, for any fixed gamma, model-0 failure matrices increase entrywise with eta, hence J_eta(gamma)>=J_0(gamma). The explicit upper bound implies V_2(eta)->L. Any sequence of optimal controllers for eta->0 has a subsequential limit whose noiseless cost is <=L by lower semicontinuity, hence lies in the rigid optimal set just proved.

It follows that, for all sufficiently small eta, every optimal controller and b=V_2(eta) satisfies
L<=b<=13/5, 3/8<=r<=5/12, 0<=s,z<=1/100, xa>=3/4,
where z=(1-s)yb. This is an existence of a fixed local neighborhood, not a claimed effective eta0.

## Quantitative local lower bound

Write delta=b-L. We have J_0(gamma)<=b. For the high-row order, the same elimination used above, with b instead of L, gives P_b(r,s,z)<=0, where
P_b=[2+4r-2s-b(1-s)(1+r)](1-bs)
 +[2-b(1-s)](br-1)(s+z)+[2-b(1-r)]z(1-bs).
Indeed 1-bs>0 and 2-b(1-s)<0 in the local box. The success cap gives r>=1/[b(1-eta)]>=1/b.

On this box, direct differentiation gives
partial_r P_b=4-b-bs+b(3-b)z >=1,
partial_s P_b=b^2-4-br-2b(b-1)s+b(b-3)z >=1,
partial_z P_b=b(3-b)(r-s) >=1/3.
These follow already from 5/2<=b<=13/5 and the displayed rational box. The coordinate path from (1/b,0,0) to (r,s,z) stays inside the box. At its start,
P_b(1/b,0,0)=1+4/b-b >=-2delta.
Thus r-1/b+s+z <=6delta; in particular br-1<=16delta and s+z<=6delta.

Now use the actual perturbed model-0 inequality. Put q0=1-eta,
alpha0=eta*r*xa+t, beta0=eta*s*ya+z.
It gives
(1-b*q0*s)alpha0 <= (b*q0*r-1)(q0*s+beta0).
The left factor is >=9/10. The right side is at most
(br-1)*2(s+z) <=192delta^2.
Hence alpha0 <214delta^2. But alpha0>=eta*r*xa>=9eta/32. Therefore eta<761delta^2, and in particular delta>=sqrt(eta)/100. No finite optimizer search is used in this inequality.

## Scope and priority

This gives a sharp exponent in the exact R79 primitive metric and already for one fixed two-label budget. It does not prove that every V_M or V_hist has the same singularity, nor improve the coefficient in the existing upper bound, nor solve finite saturation, optional commitment, the original squared-sign risk, phase-type timing, or human novelty assessment. The controller-value formula is classical absorbing-chain algebra; the addition is the global rigid optimum and matched support-changing sensitivity construction.
