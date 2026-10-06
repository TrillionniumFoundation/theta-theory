# Author-side proof audit — Revision 89

This audit accompanies written proofs. It is not an independent human priority opinion, a proof-assistant certificate, or physical execution. The controlling R58 texts and every prior mathematical section remain unchanged.

## 1. Reconciled genealogy and dependencies

The actual base is remote v88 `d1add4a7ba45230b3cba71b47ef46da5e4a88d72`, with native source `cebd9b28f8ea603fa98c8c5c8f70d9e1daafb3d1`. It contains conditional-fidelity reset width. The prior session's different local v88 allocation draft was not pushed. Seven files from it are retained verbatim in `unpublished-local-v88`; the active allocation proof is now Section 80, with a new reset-feedback upper. There is no false remote v88 ancestry.

The active new chain is: covariance and complete support kernel (67,69); actual-output correction (70); finite probability and one-sided tube (72,75,76); finite GHZ-block remainder (78); subnormalized reset accumulation and adaptive-block bound (79); unequal common readout and prescribed-profile theorem (80); hard quadratic budget, preparation-channel stability and strict memory-model comparison (81). The structural article and independent analytic programme are not logical premises. No old proof is shortened to make the new theorem appear self-contained.

## 2. Unequal common classical readout

For x_r in [0,1/2] and alpha*x_r<=u_r<=x_r, put S=sum x_r², A=max(sqrt(S),S), t_r=x_r/(16A). The case S=0 is handled before division. Then max t_r<=1/16 and sum t_r²<=1/256. Under the alternative, the complex expectation factors as product(cos t_r+2 i u_r sin t_r). Its modulus is at least product cos t_r>=1-sum t_r²/2>=1/2. The unwrapped sum of arguments obeys alpha*S/(16A)<=phi<=S/(4A)<=1/4. Hence its imaginary part is at least alpha*S/(64A). The bounded statistic sin(sum t_r X_r), converted to one randomized binary readout, is fixed by x and not by u. This proves a finite trace separation uniform in all component biases. No unknown-parameter likelihood-ratio test or equal-signal reduction is used.

## 3. Prescribed-profile upper, independent and feedback cases

For independent complete groups, the established block lemma gives Bures distance s(1.5 beta0 n_r+sqrt(r0 n_r)). The square-root term comes from the full n_r*r0*s² diamond remainder. Root fidelities multiply only between independent groups, and the trace norm is at most twice the resulting Bures distance. Euclidean triangle inequality gives 2s(1.5 beta0 sqrt(V)+sqrt(r0 N)). Public mixing has a retained common classical label and is treated by direct sums.

A prescribed-profile reset protocol need not have product outputs. The fresh adaptive-block lemma gives history-uniform deficits a_r=s²(alpha n_r+sqrt(r0 n_r))²/2. Their deterministic sum is the same on each full reservation path. Apply the subnormalized conditional-fidelity lemma, then trace/fidelity conversion and the trace cap. This proves the same finite upper without importing old receiver systems into new acquisitions. Null histories are never normalized; countably many outcomes use trace-class sums.

Regular directions instead retain the sharper horizontal upper 2 beta_h sqrt(N)s+(Lambda+K_h)N s². The substitution x=sqrt(N)s and the cap two absorb x² only when x<=1. Support openings use the fixed impossible-label lower and hybrid upper. Product-reference witnesses are allowed in every prescribed complete profile, by grouping independent pairs.

## 4. Prescribed-profile coherent lower

Each group uses m_r=min(n_r,floor(1/(2Delta*s))) logical GHZ factors, with all encodings before acquisition and recoveries after acquisition. The actual tensor channel differs by at most m_r*kappa*s². Its fixed binary event has bias within m_r*kappa*s²/2 of sin(x_r)/2, where x_r=m_r Delta s. Shrinking s0 by 1/(4Delta) and Delta/(pi kappa) gives x_r/(2pi)<=u_r<=x_r, uniformly in the allowed remainder. Apply the unequal-signal lemma before using any asymptotic notation.

If no group clips, the resulting sum is Delta*s*sqrt(V). If one clips, the floor argument is at least two and its x_r>=1/4. Since the target rate is at most one, this constant controls the saturated target regardless of the remaining allocation. Thus the coherent lower constant can be min(Delta,1/4)/(128pi). The reference dimension bound 2d is per used call, not per group. The readout depends only on the known base, tangent and public allocation/scale. It is not advice for an unknown-measurement learner.

## 5. Quadratic budgets

The sharper policy bound uses B_pi=sup_paths sum(alpha*n+sqrt(r*n))². Conditional accumulation gives min(2,2s sqrt(B_pi)); pathwise Minkowski gives alpha sqrt(Q_pi)+sqrt(r N_pi). Supremum, not expectation, is essential.

For the class N_pi<=N,Q_pi<=Q, N<=Q<=N², choose b=floor(Q/N). Then Nb<=Q and Nb>=Q/2. Packing N calls into b-sized groups gives V in [Nb/2,Nb], hence [Q/4,Q]. The prescribed-profile lower therefore attains sqrt(Q)*s up to constants. The integer witness is compressed, so polynomial represented-input arithmetic does not imply allocation of a huge explicit input state. It is a sufficient budget witness, not an exact equality V=Q. Each individual policy need not be informative, even with high Q; forgetting its output gives separation zero. No matching lower for a fixed arbitrary feedback decision tree is claimed. Coarsening gives an operational set inclusion for independent allocation testers only; removing a reset boundary can remove a receiver interaction, so no such set inclusion is inferred for arbitrary reset policies.

## 6. Certified deviation from reset

At history h assume the preparation channel differs, in uniform unhalved diamond norm, from R -> R tensor sigma_h by at most delta_h, with largest path sum epsilon. Fix either device. Backward induction for arbitrary positive incoming R pays delta_h*tr(R) at the current preparation and at most (epsilon_h-delta_h)*tr(R) for all continuation branches. Complete trace-preserving instruments make child traces sum correctly. Thus each hypothesis's final normalized state moves by at most epsilon, and comparison of two hypotheses pays 2epsilon. This is a common ideal channel hypothesis valid with all references, not a statement about marginal separability or average calibration. A fixed positive epsilon can overwhelm a shrinking local signal.

## 7. Exact memory-model inclusion and witness

Ohst et al. Definition 23 gives two-call effects sum_z R_z tensor S_i|z, so every effect is separable across complete call slots. The corresponding measure-and-reprepare realization is a unit-reset protocol, proving inclusion. Our witness instead retains two independent Bell references and measures them jointly after both classical outputs. With classical label event 00, T0=Pi^T/4 tensor |00><00| and T1=I_inputs/4 tensor I_outputs-T0 are positive with the correct deterministic tester normalization. Partial transposition of the first complete call has eigenvalue -1/8, so this tester effect cannot have the source's product decomposition. It is a valid unit-reset tester with no coherent import. The negative eigenvalue concerns the tester operator, not a claimed strict optimal-score gap for every identical-channel discrimination problem. The source's constrained-separability optimization for its smaller class cannot directly upper-bound this larger class by deleting a memory cap. We do not rule out other lifted optimization formulations.

## 8. Exact execution and preservation

`profile_check.py`: 7206 checks, 24 rejection controls, 198 complete unequal Bernoulli laws, 15 complete small GHZ profile laws, 144 certified common-readout cases. `resource_check.py`: 39787 checks, 19 rejection controls; all N,Q integer budgets through N=39; a compressed huge-integer case; shared-subtree policy and pathwise defect arithmetic; exact partial transpose; 36 channel contractions and 36 complete reset-deviation laws. Ordinary and optimized executions must agree. These are finite regression statements, not universal proof certificates.

The native inventory and active graphs are checked against `V88_BASELINE.json`. All 665 predecessor files remain represented; altered entry/audit/build files have exact copies. All predecessor mathematical sections remain byte-identical and active. Production receipts must identify the actual v89 native commit. A separate read-only final-head run, triggered on the final metadata-only head, establishes that head's reconstruction; an installed workflow or an old receipt does not do so. Neither builds nor this audit establish independent specialist priority or signed human authorship.
