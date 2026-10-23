# R74 mathematical development: contrast, quotient decompositions and exact memory transitions

Author-team mathematical development, 2026-10-20. This is a proof draft, not an independent referee report or a journal assessment. It continues the definitions and proved normal form of R73. No existing manuscript file has been edited by this agent.

## 0. Standing definitions and scope

Let `b : A* -> Delta(C)` be compactly reversible with finite minimal observable group `G`. Use the chronological right action in R73. Every group element is represented by a positive command word. Write `b(g,c)` for the resulting response table, `V=V_b` for the real cyclic observable module, `N` for the number of residuals, and

`nu_G(V) = min {|X| : V embeds as a real G-module in R^X}`.

R73 already proved

`m(b) = min{N, 1 + kappa_G(b)}`,

where `kappa_G(b)` is the least size of a finite G-set admitting `b(g)=lambda P_g D`, with a probability initial row and a row-stochastic decoder. This invariant and that normal form are inherited, not new claims below.

Let `pi=|G|^{-1} sum_g b(g)` and, for `0<=t<=1`, set

`b_t(g) = pi + t(b(g)-pi)`.

This is **terminal readout contrast**, not the length-dependent damping `alpha^{|w|}` of R73. For a prepared unitary experiment it is realized by the POVM `E_c(t)=t E_c+(1-t)pi_c I`, without changing the preparation or commands. An outcome with `pi_c=0` has `b(g,c)=0` for every g and can be removed throughout, then restored as a zero decoder column. Thus all remaining `pi_c` are strictly positive without an extra assumption.

## 1. General finite-group low-contrast theorem

### Theorem A

For every finite observable group G and every nonconstant probability response b, there is an explicitly positive `t_0` such that

`kappa_G(b_t)=nu_G(V_b)` and `m(b_t)=min{N,1+nu_G(V_b)}`

for `0<t<=t_0`. The group, residual cardinality and observable G-module of b_t equal those of b for every `t>0`. At `t=0`, the response is constant and its memory is one.

The theorem holds for arbitrary finite groups, multiple terminal outcomes and arbitrary valid probabilities. No multiplicity-free or abelian hypothesis is needed.

### Complete proof

Every f in V has a suffix-independent total output mass `ell(f)=sum_c f(z,c)`: this holds for the spanning residuals and hence for their linear combinations. The group average operator on V sends every residual to the same constant response `bar b(z)=pi`. Therefore its image is precisely `R bar b`, and

`V = R bar b direct-sum W`, where `W=ker(group average)`.

The module W has no invariant vectors, and every w in W has `ell(w)=0`.

Choose a minimum G-set X, of size k=nu_G(V), and an equivariant injection `j:W->R^X`. The permutation inner product on `R^X` is G-invariant. Averaging commutes with j, so `j(W)` is orthogonal to the entire invariant subspace, in particular to the uniform row `p=(1/k,...,1/k)`. Its rows have coordinate sum zero. Let

`F = j^{-1} composed with orthogonal projection onto j(W)`.

This map is equivariant, `F j=I_W`, and `F(p)=0`. Put `v=b-bar b`, `a=j(v)`, and define rows

`T(x,c) = [F(e_x)](empty,c)`.

Every row of T sums to zero. Also `pT=0`, and `aP_g T=b(g)-pi` by equivariance and evaluation. Choose

`epsilon = 1/(2 k ||a||_infinity)`.

The vector a is nonzero because b is nonconstant, so epsilon is defined. The row `lambda=p+epsilon a` has total mass one and all entries at least `1/(2k)`. Set

`B = max_{x,c} |T(x,c)|/pi_c > 0`,

`t_0=min{1,epsilon/B}`,

and `D_t(x,c)=pi_c+(t/epsilon)T(x,c)`. The definition of t_0 makes D_t nonnegative; its row sums equal one. A direct calculation gives

`lambda P_g D_t = pi + (t/epsilon)(pP_g T+epsilon aP_g T)=b_t(g)`.

Thus `kappa_G(b_t)<=k`. The affine map `f -> t f+(1-t)ell(f)bar b` is an invertible equivariant map of V for t>0 and sends each residual of b to the corresponding residual of b_t. Consequently the modules, group kernels and equality pattern among residuals are unchanged. The R73 module lower bound gives `kappa_G(b_t)>=nu_G(V)=k`; its exact memory formula gives the asserted pure-start minimum. At zero contrast use one label.

### Corollary: an exact obstruction surviving any nonzero readout contrast

If the compact observable group is infinite, every `b_t` with `t>0` still has that infinite observable group, so R72 rules out every finite exact stochastic realization. Constant readout at t=0 has one label. Thus a small nonzero terminal contrast can make every active output probability strictly interior while leaving exact memory infinite. This corollary is a direct application of the inherited R72 criterion, not a separate realization breakthrough.

## 2. Exact orbit absorption when stabilizers are normal

### Lemma B

Suppose a probability factorization is carried by a finite G-set whose point stabilizers are normal. It can be replaced, with no larger set, by one with at most one orbit `H\G` for each normal subgroup H and with the initial row concentrated on the identity coset inside each orbit. Only the mixture **between** its orbits remains.

### Proof

On one orbit `H\G`, let its initial mass be p>0 and normalize its local row lambda. Its response is

`q(g,c)=sum_{Hx}lambda(Hx)D(Hxg,c)`.

For h in H, normality gives `Hxhg=Hxg`, hence q(hg,c)=q(g,c). Thus q factors through `H\G`, and its values form a probability decoder on that quotient. Replace the initial row on this orbit by the point mass at H and the decoder by q. This reproduces the whole local response. If several orbits have the same H, replace them by one orbit with total initial mass and the corresponding weighted average decoder. Zero-mass orbits are deleted. The result retains every command-word response and weakly decreases the number of points.

Normality is essential to this proof; it must not be silently asserted for arbitrary stabilizers in a nonabelian group. The theorem below therefore applies globally to finite groups in which **all** subgroups are normal (Dedekind groups), in particular every finite abelian group. It also describes the exact restricted problem for normal-stabilizer cores in any finite group.

### Theorem C: subgroup LP formula and exact synthesis

Assume every subgroup of G is normal. For a nonempty set of distinct subgroups `mathcal H`, write

`cost(mathcal H)=sum_{H in mathcal H}[G:H]`.

For each H let `f_H : H\G x C -> R_+` and `p_H>=0` satisfy

1. `sum_c f_H(q,c)=p_H` for every quotient coset q;
2. `sum_H p_H=1`;
3. `sum_H f_H(Hg,c)=b(g,c)` for every g,c.

Then

`kappa_G(b)=min{cost(mathcal H): these linear constraints are feasible}`.

Moreover N=|G|, so `m(b)=min{|G|,1+kappa_G(b)}`. For rational b every minimum has an exact rational realization. For entries in a specified real algebraic number field K, a minimum realization can be chosen in the same field K; no algebraic field extension is needed to solve any of these linear programs. This concerns controller entries and exact label minimization, not an efficient bound on enumerating all subgroup families.

### Proof

Apply R73 to an arbitrary stochastic realization, then Lemma B to its permutation core. The orbit contributions give the displayed constraints. Conversely, any feasible solution has f_H=0 when p_H=0; otherwise its decoder is `D_H=f_H/p_H`. Start with mass p_H at the identity coset of each active quotient and use right multiplication as transitions. This gives b. The R73 initializer construction charges its pure start correctly.

A minimum over subgroup families exists because the regular orbit H={1} realizes b; only finitely many distinct subgroups and hence families exist. Feasible sets of the displayed variables are bounded closed polyhedra: `0<=f_H<=p_H<=1`. Linear programming over rational data has rational feasible vertices; over a real algebraic field its vertices are obtained by solving linear equations in that same field. A vertex therefore supplies the asserted entries, including the divisions by positive p_H.

To prove N=|G|, the stabilizer H_0 of b as a residual is a subgroup and hence normal. If h fixes b and g is arbitrary, normality lets h move across g as an element of H_0; therefore h fixes every residual in the orbit. The residuals span V, so h is the identity in the minimal observable group. H_0 is trivial. Orbit-stabilizer gives N=|G|.

## 3. Full payoff dual, finite lower certificates and exact thresholds

For H define the polytope `P_H` of all quotient probability tables on H\G, viewed as tables on G. Feasibility in Theorem C is exactly

`b in P_mathcalH := conv(union_{H in mathcalH} P_H)`.

Each P_H is a product of probability simplexes; its vertices choose a single outcome for each coset. Let y be any real signed table on G x C and use the unnormalized pairing `<y,b>=sum_{g,c}y(g,c)b(g,c)`. Define

`h_H(y)=sum_{q in H\G} max_{c in C} sum_{g in q}y(g,c)` and `h_mathcalH(y)=max_{H in mathcalH}h_H(y)`.

### Theorem D: exact payoff criterion

The family mathcalH is feasible if and only if

`<y,b> <= h_mathcalH(y)` for every real table y.

If it is infeasible there is a strict witness. For rational b the witness may be chosen rational. A witness with margin `Delta=<y,b>-h_mathcalH(y)>0` continues to exclude the same family for every table b' with

`||b'-b||_infinity < Delta/||y||_1`.

### Complete proof

Maximization over a quotient probability decoder chooses independently, in every coset, an outcome c attaining the indicated maximum. This proves the support function h_H. The support function of the convex hull of finitely many compact sets is their maximum, proving h_mathcalH. Membership implies every inequality. If b is outside P_mathcalH, let q be a closest point in this compact convex set. The first variation of squared distance along every segment from q to x in that set gives `<b-q,x-q><=0`. With y=b-q, one gets `<y,b>-h_mathcalH(y)>=||b-q||^2>0`. Approximate y by a rational table closely enough to preserve its strict gap when b is rational (indeed even for real b), using continuity of the finite support maximum. The perturbation bound follows from `<y,b'-b> >= -||y||_1 ||b'-b||_infinity`.

The criterion is a concrete Farkas/separation dual, not a claim that all group symmetry constraints in unrestricted nonnegative rank become linear. It depends on the proved normal-stabilizer absorption.

### Theorem E: contrast thresholds

For any finite G (not necessarily abelian), and every integer k>=1, there is `tau_k in [0,1]` such that

`kappa_G(b_t)<=k` exactly for `0<=t<=tau_k`.

There are only finitely many thresholds, `tau_k` is nondecreasing in k, `tau_N=1`, `tau_k=0` for `k<nu_G(V_b)`, and `tau_{nu_G(V_b)}>0`. For positive t the exact pure-start memory follows from `min{N,1+kappa_G(b_t)}`. Each threshold retains the lower memory at the threshold itself; a jump occurs immediately above it. For algebraic b all thresholds are algebraic and effectively decidable using the finite permutation actions and real algebraic feasibility of R73. No new general efficient quantifier-elimination claim is made.

For a group with all subgroups normal, each tau_k is obtained by finitely many **linear programs**, one for each family with cost<=k. If b is rational, every tau_k is rational and both extremal controllers and strict infeasibility certificates can be rational. In particular these need not be merely sufficient plateau cutoffs.

### Proof

For a fixed action of size<=k, the parameters lambda,D and t lie in a compact product of probability simplexes and [0,1]. The response constraints are closed, so feasible t form a compact set. If s>0 is feasible, then any `0<=t<=s` is feasible using the same lambda and decoder `(t/s)D+(1-t/s)1 pi`; hence that set is an initial closed interval. There are finitely many actions of G on at most k labelled points, so their union is another initial closed interval. Its endpoint is attained. All remaining group-general assertions follow from Theorem A, the module lower bound, the residual realization, and polynomial real-algebraic elimination. The t=0 table may have trivial observable group; kappa_G there simply allows the one fixed-point action.

For normal-subgroup groups, replace the response equations in Theorem C by `sum_H f_H(Hg,c)=pi_c+t(b(g,c)-pi_c)` and maximize t in [0,1]. This is a bounded linear program over the original coefficient field. Take the maximum over the finite collection of admissible families. Rationality and actual optimal controllers follow from linear-system vertices as before.

For a fixed nonempty family and nonconstant b, write v=b-pi. Its unclipped ray endpoint has the exact support dual

`zeta_mathcalH = inf_{<y,v>=1} [h_mathcalH(y)-<y,pi>]`,

and `tau_mathcalH=min{1,zeta_mathcalH}`.

The inequalities defining membership give the formula directly: those with `<y,v><=0` hold automatically because pi belongs to every P_H; the others may be normalized to one. The infimum is a minimum. One way to see attainment without a regularity promise is to use any finite inequality description of the polytope P_mathcalH in its affine hull. If v is outside its linear span, an affine-hull equation provides an attained value zero. Otherwise the first boundary reached along the ray activates one of its finitely many facet inequalities with positive directional coefficient. This also supplies the maximizing supporting score. Equivalently introduce variables z_Hq and s, impose

`z_Hq >= sum_{g in q} y(g,c)` for all H,q,c,

`s >= sum_q z_Hq` for all H,

and `<y,v>=1`, and minimize `s-<y,pi>`.

This is an explicit linear dual. It does not claim a polynomial total algorithm: subgroup-family selection itself is a separate finite combinatorial optimization.

## 4. Fourier module cover for abelian G

Let S be the set of complex characters whose vector Fourier coefficient in b is nonzero. It contains the trivial character and is closed under conjugation. The cyclic module is multiplicity-free: applying the character averaging projections to b obtains each nonzero character mode, and no other mode. A real conjugate pair is counted as one real two-dimensional summand.

The permutation module on H\G contains exactly the characters trivial on H, each once. Consequently

`nu_G(V_b)=min sum_H [G:H]`

over distinct subgroup families for which every active character belongs to at least one annihilator H^perp. This is a representation-theoretic cover; it is a lower bound for every contrast and equals the exact positive factorization size at all sufficiently small positive contrasts by Theorem A. It need not equal the exact answer at full contrast. The next theorem gives a sharp failure, with a complete threshold rather than an isolated example.

## 5. A sharp rational transition on C_2^4

### Theorem F

Take `G=(F_2)^4`, generated by its four coordinate flips. Let chi_1,...,chi_4 be its coordinate sign characters and `chi_5=chi_1 chi_2 chi_3 chi_4`. For `0<=t<=1` define the binary response with first coordinate

`beta_t(g)=3/8+(t/8)sum_{i=1}^5 chi_i(g)`.

For t>0 its observable group is G, its dimension is **six**, and N=16. Moreover nu=10 and

`kappa_G(b_t)=10` if `0<t<=3/5`,

`kappa_G(b_t)=12` if `3/5<t<=1`.

The pure-start stochastic memory is therefore exactly eleven and thirteen respectively; at t=0 it is one. In particular no twelve-label minimum occurs anywhere in this family. All realizations displayed below have rational entries whenever t is rational. This is a special exact family inside the preceding general theorems, not a universal closed formula for all groups.

### Validity, observability and the module lower bound

The five signs have product one, so their sum is 5,1 or -3. Thus beta_1 takes values 1,1/2,0, and beta_t is its convex combination with 3/8. Any four of the five characters are linearly independent over F_2, and all five have the unique relation that their product is trivial. For t>0 their five Fourier coefficients and the constant coefficient are nonzero. This gives dimension six. Their joint kernel is trivial; for an abelian group this is also the stabilizer of the initial residual, so N=16.

Write W=H^perp for a quotient orbit, and let r=dim W; its size is 2^r. A proper W contains at most r of the five active nontrivial characters, because every set of at most four is independent. For r=1,2,3 its cost satisfies `2^r>=2r>=2|W intersect S_nontrivial|`. The full r=4 orbit has cost16. Any collection covering all five thus costs at least10, while the five individual two-point quotients give cost10. Hence nu=10.

### Lower bound excluding every core of size at most eleven above 3/5

By Theorem C, it is enough to consider distinct quotient orbits and their nonnegative subprobability contributions f_H. A core of size<=11 cannot contain a size16 orbit. A size8 orbit covers at most three of the five active characters; the remaining budget is at most3 and covers at most one more, so it cannot occur. The nontrivial orbits therefore have sizes2 and4. They have cost exactly twice the dimension of W. Covering all five requires total nontrivial cost at least10. The budget11 leaves at most one fixed point and forces each size2 or size4 orbit to cover respectively one or two active characters, with no repeated coverage. Thus the active characters are partitioned into blocks of size one or two.

For a two-character block `{chi_i,chi_j}`, the annihilator also contains their product. That product is not active. Products arising from different pairs are different: equality would give a nonempty relation involving at most four of the circuit characters. It belongs to no other chosen annihilator, since those have just their own one- or two-character block and its pair product. Therefore its coefficient in f_H must be zero. For a one-character block there is no other nonconstant mode. The first-output contribution on each orbit is consequently

`f_H(g,1)=a_H+(t/8)sum_{i in I_H}chi_i(g)`.

The characters in a block are independent, so they simultaneously take value -1 on some coset. Nonnegativity implies `a_H>=|I_H|t/8`. Sum over the five covered characters. A possible fixed orbit contributes a nonnegative constant. Since the target mean is3/8,

`3/8>=sum_H a_H>=5t/8`.

Thus t<=3/5 is necessary for every size<=11 core, establishing the strict higher-region lower bound. This proof is an exact Fourier/positivity certificate; it does not depend on a numerical LP infeasibility result.

### Matching ten- and twelve-point constructions

For `0<t<=3/5`, use five two-point quotient orbits, initialize mass1/5 at the plus point of each, and give orbit i first-coordinate decoder

`D_i(g,1)=3/8+(5t/8)chi_i(g)`.

It lies in [0,1] throughout the asserted interval; the weighted response is beta_t. This attains kappa10 and, after the charged initializer, m11.

For t=1, use one four-point quotient on `(chi_1,chi_2)` and one eight-point quotient on `(chi_3,chi_4,chi_5)`, with initial mass1/2 at the all-plus point of each. On the first orbit let the decoder be the indicator that both signs are plus. On the second let it be the indicator that at least two of its three signs are plus. If a,b,c are sign variables, the majority indicator is

`1/2+(a+b+c-abc)/4`.

The two weighted decoders add to

`(1+chi_1+chi_2+chi_1 chi_2)/8 + 1/4 +(chi_3+chi_4+chi_5-chi_3 chi_4 chi_5)/8`,

which is beta_1 because `chi_1 chi_2=chi_3 chi_4 chi_5`. For general t replace each decoder D by `(1-t)3/8+tD`; all decoder rows remain valid and the response is beta_t. This gives kappa<=12 for every t, proving equality above3/5. R73 charges one initializer because N16 exceeds both core costs plus one.

### Physical implementation and claims that are not made

There is an immediate prepared sixteen-dimensional diagonal quantum realization: start at the identity basis state, use regular permutation unitaries for the four generators, and take the diagonal terminal effect with entries beta_t(g). This is already a classical realization. No small-dimensional quantum advantage is claimed. Its purpose is the exact arbitrary-stochastic memory lower bound and the separation between a fixed observable module and the bounded-positive decoder constraint.

## 6. Priority audit and distinctions

The proof drafts above use elementary finite representation theory, group actions, finite convex separation and linear programming. Those ingredients are classical. The novelty claim should be confined to their proved consequences for the R73 **all-word stochastic memory with pure-start charge**, the normal-subgroup orbit absorption giving an exact LP reduction, and the exact positivity threshold family; do not claim the invention of equivariant factorizations, convex lifts, barycentric perturbations, or low-rank positive realizations.

Primary sources read online during this work:

1. Gouveia, Parrilo, Thomas, *Lifts of convex sets and cone factorizations*, Mathematics of Operations Research 38 (2013),248-264. https://arxiv.org/pdf/1111.3164 . Theorem2.4 relates cone lifts to slack-operator factorizations; Theorem2.12 gives the symmetric version using a group homomorphism and equivariant factor maps. This is the relevant classical geometric framework. A probability response table is not automatically the complete slack operator of its residual polytope, and its common G-action plus pure-start memory charge must still be proved.

2. Kaibel, Pashkovich, Theis, *Symmetry matters for sizes of extended formulations*, SIAM Journal on Discrete Mathematics26(3) (2012),1361-1382. https://arxiv.org/pdf/0911.3712 ; publisher DOI10.1137/110839813. The publication metadata were corrected against the publisher's record at https://epubs.siam.org/doi/10.1137/110839813 during the final handoff; the earlier draft's volume25/year2011/pages1513-1537 were erroneous. In particular Definition11 and Lemma12 concern coordinate-symmetric sections. Symmetry-constrained positive lifts and their extra cost are established themes, not new general phenomena being claimed here.

3. Gillis, Glineur, *On the geometric interpretation of the nonnegative rank*, Linear Algebra and its Applications437 (2012),2685-2712. https://arxiv.org/pdf/1009.0880 . Restricted nonnegative rank imposes an equality of factor and target linear spaces; its geometry warns against identifying arbitrary positive factorizations with vertices in the minimal observable space. R73 already avoids that error through its recurrent projection, and the present proofs use its normal form instead of silently adding a restriction on hidden-state responses.

4. Bocci, Carlini, Rapallo, *Perturbation of matrices and nonnegative rank with a view toward statistical models*, SIAM Journal on Matrix Analysis and Applications32 (2011),1500-1512. https://arxiv.org/pdf/1010.3566 . Theorem3.1 and Proposition3.2 establish local nondecrease and barycentric perturbation behavior for ordinary nonnegative rank. Hence preservation of a positive-factorization lower obstruction under small perturbations and monotonicity under mixing are not presented as new general principles. The theorem above adds the exact permutation-module value under small terminal contrast while maintaining one common group action and the charged start.

The search also found Gillis's SIAM monograph discussion of rank-one perturbations reducing nonnegative rank to ordinary rank. The author-hosted full PDF could not be downloaded (web-tool size limit; direct HTTP503), so this draft does not claim inspection of its Theorem3.3 or trace its original priority. The four successfully opened primary papers are sufficient to acknowledge the verified relevant framework. No exhaustive priority clearance or independent specialist approval is claimed.

## 7. Suggested finite diagnostics, separate from the proofs

Use exact rational arithmetic to enumerate all67 subspaces of F_2^4, verify the five-character circuit, its 16 response values, all quotient character supports, the ν=10 covering lower bound, the size<=11 orbit classification, the disjoint inactive pair products, the decoder thresholds at0,3/5,1, and both all-word constructions by checking the16 group elements and their four generator transitions. The group action makes these finite table identities equivalent to all words **for the displayed constructed machines only**. The universal lower bounds remain the written proofs above. A numerical LP may independently reproduce the threshold but must not be called a formal proof certificate unless its exact rational primal/dual values are reconstructed and checked.
