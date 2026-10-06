# Proof and resource audit — Revision 88

This is an author-side audit of written mathematics. It is not an independent referee judgment, a proof-assistant certificate, a physical demonstration, or a priority clearance. The complete R57 reports were read at immutable remote commits; they are referenced, not falsely represented as locally frozen downloads.

## 1. Prescribed complete groups

The new definition fixes a nonempty finite list of positive group sizes. All input-reference systems factor across the groups, conditionally on a public classical randomization record. Entanglement and reference dimensions within each group and final joint processing are unrestricted. A common quantum reference linking nominal groups is excluded. Padding and discarding permit smaller effective use of an allocated group without introducing feedback.

The theorem fixes E,H!=0,Lambda. H is a Hermitian zero-sum tuple in the one-sided positive-semidefinite tangent cone. All legal F satisfy the complete sum-operator-norm remainder inequality. Constants are uniform in F, s in the stated interval and every allocation, not in E,H,Lambda. The interval for the previously proved sufficient realization need not be the discrimination interval.

## 2. Common readout for unequal signals

Let independent signs have alternative means 2u_r, with alpha*x_r<=u_r<=x_r<=1/2, and base means zero. Set S=sum x_r², A=max(sqrt(S),S) and t_r=x_r/(16A), with the zero-S case separate. Then t_r<=1/16 and sum t_r²<=1/256. The bounded statistic is sin(sum t_r X_r), independent of the unknown biases.

Its characteristic expectation is the product of cos(t_r)+2i*u_r*sin(t_r). Every factor has positive real part. The product modulus is at least product cos(t_r)>=1-sum t_r²/2>=1/2. The summed arguments are between sum u_r t_r and four times that sum, hence between alpha*S/(16A) and S/(4A)<=1/4. There is no uncontrolled phase wrapping despite an arbitrary number of blocks. The sine lower on this interval gives expectation at least alpha*S/(64A). Under the fair law the expectation is zero by symmetry. Randomized acceptance with probability (1+statistic)/2 has unhalved binary separation equal to the expectation difference. This proves the full finite lower, with no use of an asymptotic normal approximation or a hypothesis-specific likelihood ratio.

## 3. Profile-sensitive finite upper

For a group of n_r calls, the canonical generally nonhorizontal factor supplies displacement at most (3/2)*beta_0*n_r*s. The full channel remainder n_r*r_0*s² contributes at most s*sqrt(r_0*n_r) in Bures distance. We use root fidelity f and beta²=2(1-f), so beta²<=unhalved trace norm<=2*beta. Fidelity multiplies only across independent group outputs. Squaring and summing the finite group bounds then gives

```
D^n <= min(2, 2s [sum_r (1.5 beta_0 n_r + sqrt(r_0 n_r))²]^(1/2))
     <= min(2, 2s [1.5 beta_0 sqrt(V) + sqrt(r_0 N)]).
```

The second line is Minkowski in the Euclidean space indexed by groups. N<=V. Direct sums with common weights handle the retained public record; final joint processing contracts trace norm. The regular upper uses the distinct horizontal solution and retains 2*beta_h*sqrt(N)*s+(Lambda+K_h)*N*s². The opening upper is the inherited hybrid bound.

## 4. Unequal coherent lower and clipping

The inherited support-complement encoding and completed recovery depend on E,H, not the remainder. The logical tensor channel for m calls is within m*kappa*s² of the ideal, with kappa=Lambda+2||Gamma||op² and logical gap Delta>0. All encodings precede acquisition; all recovery follows it. This is a tensor power and not an implicitly sequential protocol. The reference bound 2d is per used call, not per entire block or gate circuit.

Choose s0<=1/(4Delta) and s0<=Delta/(pi*kappa), as well as the inherited factor interval. In every allocated group put m_r=min(n_r,floor((2Delta*s)^-1)) and x_r=m_r*Delta*s. The fixed Pauli-Y event, extended by zero off the GHZ span, is a legal complete-space effect. Its base probability is 1/2 and its alternative bias obeys

```
|u_r-sin(x_r)/2| <= m_r*kappa*s²/2,
x_r/(2pi) <= u_r <= x_r,
0<x_r<=1/2.
```

Pay this error inside each bias before amplification. The preceding common-readout lemma gives (128pi)^-1*min(1,Delta*s*sqrt(sum m_r²)) using a single test for every permitted F.

If no group clips, this controls min(1,s*sqrt(V)) with factor min(1,Delta). If any group clips, the floor argument is at least two and that group's x_r is at least 1/4. The lower is a fixed positive constant while the target is at most one. This covers arbitrary unequal or growing groups with no dyadic grouping factor. One valid coherent lower constant is min(Delta,1/4)/(128pi). Neither the blocks nor the final statistic use the unknown remainder.

## 5. Other rows and budget consequences

Independent product inputs and their fixed events belong to every prescribed allocation; every allocation is allowed by an adaptive tester. The previously proved regular and opening bounds therefore sandwich both rows at the asserted scales. This preserves the classical impossible-output mechanism of support opening, distinct from coherent correction.

For a total budget N and width b, transferring a slot from a smaller unfinished group to a larger one cannot decrease the squared sum. Maximization yields q groups b and remainder r, with Vmax=q*b²+r², q=floor(N/b),r=N-q*b. Since r<b<=qb, Vmax>=Nb/2; the upper is Vmax<=Nb. This optimizes an allocation budget. A prescribed allocation's effective width V/N can be much smaller than its largest group. Merging groups is an operational inclusion and adds 2uv to V.

## 6. Relation to known tools

The second-moment metrological mechanism, corrected phase accumulation, fidelity multiplication and isometric comparisons are established ingredients, not new principles by themselves. `editions/channel-bures-comparison88.tex` states the precise HMNW/Yuan–Fung inequalities and the substitution yielding the inherited one-group upper. The new lower is a written finite, common-event synthesis for unequal independent signals and the whole fixed tube. No novelty is inferred from an absence of search hits.

## 7. Exact executed scope

`profile_geometry.py` computes N,V,V/N, the exact budget maximizer, and optional public phase-clipping data on represented inputs. It classifies no measurement, evaluates no adaptive distance, computes no local interval, and synthesizes no recovery. The optional clipping checks the phase bound only, not the separate quadratic remainder condition. Typed complete JSON replay rejects extra, missing, changed or type-substituted fields; incomplete input caps refuse rather than truncate. Maximum profiles are run-length encoded, so a large binary-encoded N does not allocate N entries.

The new suite checks all ordered integer compositions through ten calls, exact unequal Bernoulli laws, complete unequal-block qubit laws, parity sufficient statistics, clipping transitions and malformed/tampered certificates. A further 144 cases evaluate the common sine readout with rational weights and a rigorous ninth-order Taylor error bound; counts are in the executed regression output. These finite tests do not prove the continuum theorem. All 25 predecessor suites execute anew.

## 8. Source and release boundaries

The authenticated v87 publication artifact supplies the exact 632-file native baseline. Every old mathematical section remains byte-identical and active. The complete 962-label graph, joint quantitative 475-label graph and structural 116-label graph are preserved. Altered entry/audit/build files are saved under `predecessor-v87-audit/`.

The initial v88 build is local and based on an artifact-import Git repository, not a reconstructed claim of actual GitHub ancestry. A locally qualified source commit and read-only local rebuild establish only those local facts. Independent remote verification, remote write completion, and cryptographic human authorship remain unestablished until actually executed. The supplied deployment procedure requalifies source in a real clone and rejects an unrelated remote base. No v87 execution evidence is reused as v88 qualification. The five independent analytic aggregate flags are unchanged and false.
