# First-order rigidity of asymptotically optimal two-label controllers

This is an author research addition, not a referee report. It is based on the exact source c0ac246181c2f4214e3e830952386adffb7d82df, Section 57 of General Theta Foundations I R80. It does not repeat the newly published value asymptotic as a new discovery. The additional conclusion is a necessary-and-sufficient characterization of all asymptotically optimal controller families to their first nontrivial orders. No independent mathematical verification of this addition has yet been recorded.

## Data and inherited inputs

Use exactly the two-model scalar instruments, compulsory success stopping, unit costs, prescribed pure initial label and arbitrary six stochastic controller coordinates from Section 57. The success table is (1-epsilon,0) in model 0 and (0,beta) in model 1, where beta=1/4 and q=3/4. The coordinates are r,s (command-a probabilities), alpha,gamma (transitions 1 to 2 following a,b failures), xi,delta (transitions 2 to 1 following a,b failures). All coordinates belong to [0,1]. There is no external clock or private persistent seed.

Let r0=(sqrt(65)-1)/32, B0=1/r0, D=beta+q*r0, A=1/r0^2, F=beta/D^2, L=q*r0^2/(beta*D^2), k=sqrt(F/(A*L))=beta/sqrt(q), h=(1/k-L*k)/(A+F), and c0=2*sqrt(F*A*L)/(A+F). All A,F,L,k are strictly positive. Put also

S=r0/(beta*D), Z=r0^2/D^2, T=r0^2/(beta*D^2), E=(1-r0)/r0.

In particular S-L=r0/D^2>0 and Z,E>0.

The proof uses three exact inherited statements, all in Section 57:
1. The baseline robust optimum B0 and its full six-parameter equality set: r=r0, s=gamma=delta=0, alpha=1, xi arbitrary.
2. Baseline local coercivity: for baseline robust excess Delta, s+delta=O(Delta), gamma=O(Delta(s+delta)), |r-r0|=O(Delta), uniformly near that equality set.
3. The value asymptotic V2(epsilon)=B0+c0*sqrt(epsilon)+o(sqrt(epsilon)).
These are dependencies, not assumptions introduced to conceal an unresolved proof: R80 states and proves them in lemmas r80-boundary-rigidity, r80-boundary-coercivity and theorem r80-sharp-modulus. The result below does not extend their instrument or memory scope.

## Proposition

Let a controller Theta_epsilon be selected for every sufficiently small positive epsilon, with no continuity or differentiability of this selection required. Let J_epsilon be its worst model expected cost, interpreted as +infinity for an improper model. The following are equivalent as epsilon decreases to zero:

(i) J_epsilon-V2(epsilon)=o(sqrt(epsilon)).

(ii) Its six coordinates satisfy

r=r0+h*sqrt(epsilon)+o(sqrt(epsilon)),
s=o(sqrt(epsilon)),
delta=k*sqrt(epsilon)+o(sqrt(epsilon)),
gamma=o(epsilon),
1-alpha=o(sqrt(epsilon)),

while xi may be any [0,1]-valued function of epsilon.

Every exact optimizer satisfies these expansions. The conclusion also implies that each of its two model costs is B0+c0*sqrt(epsilon)+o(sqrt(epsilon)). The statements concern a fixed labeling with initial label 1, not an uncounted mixture of starts.

## Proof: localization and missing scale

Write lambda=sqrt(epsilon). Suppose (i). By inherited input 3,
J_epsilon=B0+c0*lambda+o(lambda).
For each fixed controller the baseline model-0 failure matrix is entrywise at most its perturbed matrix. Its baseline robust cost J_0 is therefore at most J_epsilon, by termwise monotonicity of the finite-prefix nonnegative cost series. Also J_0>=B0. Any accumulation point of Theta_epsilon in the compact parameter cube is a baseline optimizer: baseline total cost is the supremum of continuous finite-prefix costs and hence lower semicontinuous. The equality set in input 1 implies
r->r0, s,gamma,delta->0, alpha->1,
without restricting xi. Coercivity then gives, uniformly,
r-r0=O(lambda), s+delta=O(lambda), gamma=O(lambda^2).

Let C1 denote model-1 cost and let C1^I be the cost after setting alpha=1,xi=0 only. For small epsilon, r>s, so this update improvement reduces C1. Both row success probabilities beta(1-r), beta(1-s) are bounded below by a common positive constant; hence all model-1 resolvents in this neighborhood are smooth and proper for all xi. With
u=beta(1-r), v=beta(1-s), a=r*alpha+q*(1-r)*gamma, b=s*xi+q*(1-s)*delta,
model-1 cost is (v+a+b)/(u*v+u*b+v*a). Differentiation in the off-diagonal probabilities gives
partial_a C1=(u-v)(v+b)/(u*v+u*b+v*a)^2,
partial_b C1=(v-u)*a/(u*v+u*b+v*a)^2.
Consequently partial_alpha C1 is negative and tends uniformly in xi to -Z at the boundary. Shrinking the fixed neighborhood, -partial_alpha C1>=Z/2. Increasing xi cannot reduce C1. Integrating first in alpha, then improving xi to zero yields
C1-C1^I >= (Z/2)*(1-alpha).
The improved cost is a smooth function of r,s,gamma,delta, equals B0 at their boundary values, and is B0+O(lambda) by the previously established scales. Since C1<=J_epsilon=B0+O(lambda), it follows that 1-alpha=O(lambda). This step is necessary; mere convergence of alpha does not justify its first-order Taylor expansion.

## Proof: subsequential expansion

Take any sequence epsilon->0 and extract a subsequence on which all bounded scaled coordinates and xi converge:
(r-r0)/lambda->H, s/lambda->u, delta/lambda->v,
gamma/lambda^2->G, (1-alpha)/lambda->a, xi->zeta.
Here u,v,G,a>=0 and zeta in [0,1]. Put t=u+v. We claim t>0.

For model 0 put
h1=(1-epsilon)*r, h2=(1-epsilon)*s,
t1=epsilon*r*alpha+(1-r)*gamma,
t2=epsilon*s*xi+(1-s)*delta,
Delta0=h1*h2+h1*t2+h2*t1.
Finite cost and alpha->1 force s+delta>0 for small epsilon: otherwise label 2 is dark and absorbing, yet is reached with positive probability epsilon*r*alpha. Then Delta0>0. The exact two-row resolvent gives
C0-1/h1=(h1-h2)*t1/(h1*Delta0).
Since Delta0<=C*(s+delta), t1>=epsilon*r*alpha, h1-h2 is bounded below positively, and h1 is bounded above and away from zero, the right side is at least c*epsilon/(s+delta). Also 1/h1=B0+O(lambda). Thus bounded (J_epsilon-B0)/lambda excludes t=0.

Now Delta0/lambda->r0*t, t1/lambda^2->r0+(1-r0)*G, and 1/h1=B0-A*H*lambda+o(lambda). The exact limit, not just a discarded positive-term lower bound, is
(C0-B0)/lambda -> X=-A*H+(1+E*G)/t.

The model-1 expression is smooth in the five small deviations uniformly over xi in [0,1]. Its derivatives at the boundary, with xi fixed, are
partial_r=F, partial_s=S+T*xi, partial_delta=L,
partial_alpha=-Z.
The gamma term is O(lambda^2). Uniform Taylor expansion therefore gives
(C1-B0)/lambda -> Y=F*H+S*u+L*v+Z*a+T*zeta*u
                      =F*H+L*t+(S-L)*u+Z*a+T*zeta*u.
The derivative identities follow either from the preceding resolvent or by differentiating its positive-denominator rational expression. In particular no differentiability of Theta_epsilon is used.

Since the normalized robust cost tends to c0, max(X,Y)=c0. Using positive weights F/(A+F) and A/(A+F),

c0 >= [F*X+A*Y]/(A+F)
   = [F/t+A*L*t]/(A+F)
     + [F*E*G/t+A*(S-L)*u+A*Z*a+A*T*zeta*u]/(A+F)
   >= 2*sqrt(F*A*L)/(A+F)=c0.

Every added term is nonnegative. Equality in the arithmetic-geometric mean forces t=k. Since E,S-L,Z are positive, equality also forces G=u=a=0. Thus v=k. Equality in the positive weighted average of X,Y under their maximum forces X=Y=c0. Solving -A*H+1/k=F*H+L*k yields H=h. Every convergent scaled subsequence has these same limits, so the full limits hold, proving (ii). No limiting restriction on xi is obtained or needed.

## Proof of sufficiency

Assume (ii). Then delta is positive for all sufficiently small epsilon. Also r->r0 in (0,1), alpha->1, s->0. Model 0 can leave label 2 through a b-failure with probability (1-s)*delta>0, then succeed at label 1 with probability (1-epsilon)*r>0. Model 1 has both row success probabilities bounded positively. Thus both model costs are finite.

The exact model-0 expansion above now applies with H=h,t=k,G=0, and gives (C0-B0)/lambda->-A*h+1/k=c0. The uniform model-1 Taylor expansion applies with u=a=0 and v=k, and gives (C1-B0)/lambda->F*h+L*k=c0, regardless of xi. Hence J_epsilon=B0+c0*lambda+o(lambda). Input 3 proves (i).

## Scope and remaining limits

This is uniqueness of the leading repair mechanism in one fixed two-label family, not a universal classification of primitive degeneracies. It does not strengthen R80's uniform value exponent, determine the best universal constant, give exact finite-epsilon controllers, solve the general-M original squared-sign risk, or settle journal significance. It makes precise that a near-optimal repair uses the b-failure return delta at scale sqrt(epsilon); making label 2 successful through s at that scale, baseline leak gamma at scale epsilon, or an alpha deficit at scale sqrt(epsilon) incurs a strictly positive leading penalty. The unused limiting xi direction stays free.
