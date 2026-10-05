# Written-proof audit — Revision 80 / R51

This is author-side mathematical cross-review of the active sources. The governing R51 reports review v77; the immediate source predecessor is published v79 `0daec5b3e20e5bf778caa90a0cf54f26c1ea53fe`, native source `4b6b43020067df10a4a21e3258c6641698b9cbc0`. Neither internal agents nor CI constitute an independent human priority opinion or an external review of v80.

The actual Sections 62 and 63 were read independently of their authors' explanations. Their source-specific audits are `CONFIDENCE_LEARNING_AUDIT.md` and `EFFECTIVE_LEARNING_AUDIT.md`. The v79 interior-code audit is reproduced below; the full inherited geometry, entropy, calibration, qubit, matrix-code, block and finite-control audits remain at their exact predecessor paths, including `predecessor-v78-audit/PROOF_AUDIT.md` and `predecessor-v79-audit/PROOF_AUDIT.md`. No old proof section is replaced by an audit statement.

## 1. Scope and active ranges

| Claim | Range | Result and boundary |
| --- | --- | --- |
| `lem:diagonalconfidence80` | `d,N>=1`, `0<delta<=2^-13`, `0<eta<=1/8` | `Omega(dN delta^-2 log(1/eta))` even for coherent adaptive training; known-basis diagonal interior hard family |
| `lem:binaryconfidenceupper80` | `d>=1`, `0<epsilon<=1`, `0<eta<=1/8` | Legal common binary estimate using `O(epsilon^-2[d^2+d log(1/eta)])` fresh Choi calls; ideal trusted operations |
| `thm:interiorconfidence80` | Same interior small-error/confidence range, every `d,N>=1` | Matching absolute-constant `N delta^-2[d^2+d log(1/eta)]`; upper fresh one-call, lower arbitrary coherent |
| `cor:operatorconfidence80` | `0<epsilon<=2^-14`, `eta<=1/8` | Same joint dimension/accuracy/confidence law for complete-body binary operator-norm learning |
| `cor:interiorconfidencecode80` | Rational `delta<=2^-13`, positive `eta<=1/8` | Joint query and deterministic-public-word rates; ideal finite Borel readout |
| `lem:algebraicreadout80` | Finite rational centres, rational `a>0` and `0<alpha<1` | Decidable uniform readout feasibility and computable algebraic feasible operators, valid for all real target effects |
| `thm:effectiveinterior80` | Rational positive `delta<=2^-13` and `eta<=1/8`, integers `d,N>=1` | Finite computable specification and finite trusted controls at the same optimal joint query/payload orders |

The target interior is `I/4<=E<=3I/4`. The device remains ordered binary, memoryless, consuming and classical-output. The future loss is unhalved adaptive `d_N` with external references and public bounded stopping. The complete-body upper is improved by choosing between the one-call Choi construction and the retained cap-`b` construction; its joint dimension dependence remains unmatched by the lower. It does not extend zero-failure learning; the retained supplied-target prefix theorem has its own `eta=0` case.

## 2. The confidence converse

### 2.1 Hard family and future separation

Set \(\Delta=512\delta/\sqrt N\le1/16\), \(E_0=I/2\), and
\(E_i=I/2+\Delta|i\rangle\langle i|\).
Every effect lies in the fixed interior. Repeating \(|i\rangle\) gives Bernoulli products whose comparison parameter is at least \(256\delta\). The inherited coefficient \(1/64\) and \(256\delta\le1\) therefore give actual future distance at least \(4\delta\).

Only this separation uses pair-dependent probes. The learning procedure does not receive the identity of the tested alternative.

### 2.2 Revealed-label extension for different current inputs

The proof extends a diagonal measurement by retaining the computational input-basis label \(J\). Tracing that label out gives exactly the original reference-assisted channel. The original controls ignore it, while the proof retains all such labels for relative entropy.

For two arbitrary current input/reference states \(\rho_0,\rho_i\), let \(\tau_j^s=\langle j|\rho_s|j\rangle\). The common map taking the input to its subnormalized basis blocks contracts relative entropy. Attaching a conditional Bernoulli bit adds the weighted classical coin divergence. Thus
\[
 D(\widetilde{\mathcal M}_0(\rho_0)\|
   \widetilde{\mathcal M}_i(\rho_i))
 \le D(\rho_0\|\rho_i)+
       \kappa_\Delta\operatorname{tr}\tau_i^0,
 \quad
 \kappa_\Delta=-\tfrac12\log(1-4\Delta^2)\le3\Delta^2.
\]
The calculation allows unequal, parameter-correlated input states and arbitrary retained quantum memory. It does not multiply unconditional observations or assume that an adaptive quantum input is independent of the parameter. Starting at common initial resources also ensures finite divergence inductively; the Bernoulli parameters stay strictly inside their support.

All intervening controls are common channels. Padding stopped paths to the cap \(M\) with ignored calls yields
\[
 D(\Omega_0\|\Omega_i)\le3\Delta^2\mathbb E_0T_i,
 \qquad\sum_i\mathbb E_0T_i=M.
\]
Crucially, the null experiment is the same for every alternative; its coordinate counts can therefore be summed. General classical outcomes are covered by the cq chain-rule formulation.

### 2.3 Testing and the sum over coordinates

Choose the null hypothesis precisely when the returned legal effect lies in its closed radius-\(\delta\) ball. Hybrid continuity makes this a measurable test, and the separation makes both errors at most \(\eta\). Data processing gives
\[
 D(\Omega_0\|\Omega_i)
 \ge(1-\eta)\log(1/\eta)-\log2
 \ge\tfrac12\log(1/\eta)
\]
for \(\eta\le1/8\). Summing proves
\[
 M\ge\frac{dN}{6\cdot512^2\delta^2}\log(1/\eta).
\]
The inequality is valid also at \(d=1\). Combining with the retained \(d^2N\delta^{-2}\) lower bound uses \(\max(u,v)\ge(u+v)/2\), not multiplication of unrelated lower bounds.

## 3. Confidence upper and future-loss transfer

The imported binary MB upper is used with seed failure \(q_d=2^{-3d}\) and operator accuracy \(\epsilon/3\). Its strict condition holds because
\(4d^2-3d\log2-\log4>0\) for every \(d\ge1\). Each seed costs \(O(d^2\epsilon^{-2})\).

Let \(k\) be the least positive odd integer at least
\(2d^{-1}\log_2(1/\eta)\). Select the first returned effect with more than \(k/2\) neighbours at operator distance at most \(2\epsilon/3\); if none exists, return the first effect. When a majority of seed outputs are within \(\epsilon/3\) of the target, a selectable centre exists. Every selectable centre has a good neighbour, and its error is at most \(\epsilon\). Legality holds on every record.

Independence comes from explicitly fresh complete seed runs. Their majority-failure probability is bounded by
\[
 2^k q_d^{k/2}\le2^{-dk/2}\le\eta.
\]
Together with \(k<2d^{-1}\log_2(1/\eta)+2\), this gives the additive \(d^2+d\log(1/\eta)\) cost. Pairwise norm tests and fixed tie selection are Borel; this ideal statistical statement alone does not compute the imported measurement entries.

For the interior future-loss theorem, \(\epsilon=\delta/(8\sqrt N)\) places successful output and target in \([I/8,7I/8]\). The retained dimension-free metric comparison gives future error at most \(\delta/2\). The upper has fresh one-call acquisition, so every permitted cap \(b\) contains it; the lower allowed all coherent training. The scalar specialization and confidence crossover \(\log(1/\eta)\asymp d\) are consistent.

The \(N=1\) specialization uses the exact identity \(d_1=2\|\cdot\|_{\rm op}\). The complete-body block lower combines the dimension, coordinate-confidence and projective-block bounds by a maximum-to-sum bound with a smaller absolute constant. It does not claim a matching complete-body dimension upper.

## 4. Learning into the retained public word

At operator accuracy \(\delta/(64\lceil\sqrt N\rceil)\), spectral clipping of a legal estimate to the target interior changes it by at most its estimation error on success. Weyl's inequality and a triangle bound give twice that error from the target. No global operator-Lipschitz claim for clipping is invoked.

The Section61 dictionary has coding error at most \(5\delta/16\). Clipping contributes at most \(\delta/8\), hence total error at most \(7\delta/16\) on the original learning success event. Rounding and fixed dictionary selection are a Borel finite partition; incorporating them into the final POVM introduces neither new device calls nor an exact-real side channel to the decoder.

The deterministic word has \(d^2\log_2(\sqrt N/\delta)+O(d^2)\) bits uniformly in dimension. Positive success for every target forces a fixed decoder's finite range to cover the interior, so its length lower is the retained entropy lower. Randomized expected-prefix descriptions use a separate converse and are not silently included in this fixed-decoder argument.

## 5. Effective readout synthesis

### 5.1 Correct classical–quantum record

For \(m\) independent maximally entangled pairs, the record after the probe queries is a direct sum over the classical bit string:
\[
 \Gamma_m(E)=\bigoplus_y d^{-m}
               \bigotimes_{\ell=1}^m E_{y_\ell}^{\mathsf T}.
\]
The blocks are subnormalized. No unknown outcome probability is divided out. Their entries are rational polynomials in the \(d^2\) real coordinates of \(E\).

For every string \(y\), a conditional final POVM has
\(A_{j,y}\succeq0\) and \(\sum_jA_{j,y}=I_{d^m}\).
These constraints are imposed even on strings of zero probability for some targets. A general collective readout can be dephased in the already-classical string without changing probabilities, so this form does not assume coherent access to device output bits or to its environment.

### 5.2 Exact uniform risk predicate

The probability \(p_j(E;A)=\sum_y\operatorname{tr}(A_{j,y}R_y(E))\) is polynomial in the relevant real coordinates. A centre is good when both \(aI-(E-C_j)\) and \(aI+(E-C_j)\) are PSD. Equality is good. For every subset of indices, the formula specifies exactly which centres are good and requires their total probability to be at least \(1-\alpha\).

Thus the indicator-defined probability is represented by a finite Boolean combination of polynomial predicates, with the correct strict complement at the boundary. Full PSD constraints use all principal minors or an equivalent real representation; a two-by-two prefilter would not suffice.

Quantifier elimination removes the universal unknown-effect variables while leaving the readout entries as free variables. Nonempty rational semialgebraic feasibility has an algebraic point. Effective enumeration and exact algebraic sign decisions select one. Equivalence over the reals ensures that this point works for all real effects, not only algebraic ones. The unknown effect is never supplied to the offline procedure.

### 5.3 First feasible size and resource bound

At each integer \(m=1,2,\ldots\), decide feasibility before searching for a witness. This avoids an unbounded witness search at an infeasible size. All computation occurs before any unknown-device access.

Use the public dictionary from Section61, \(k_N=\lceil\sqrt N\rceil\), \(a=\delta/(8k_N)\) and \(\alpha=\eta/2\). The Section62 estimator at \(\epsilon=\delta/(64k_N)\) followed by clipping and dictionary rounding has operator error at most
\[
 2\epsilon+5\delta/(64k_N)
 =7\delta/(64k_N)<a
\]
on its success event. Its finite Borel readout therefore supplies a feasible POVM at some
\(m_0=O(N\delta^{-2}[d^2+d\log(1/\eta)])\).
Only existence is used; no unproved computation of its operator integrals is assumed. The first feasible \(M\) is at most \(m_0\).

The selected readout has ideal failure at most \(\eta/2\) for operator radius \(a\), implying future error at most \(\delta/2\). Its entries are computed algebraic numbers, not arbitrary unrepresented reals.

### 5.4 Finite trusted controls

For each \(y\), the algebraic isometry
\[
 V_y\psi=\sum_j|j\rangle_C|j\rangle_Z\sqrt{A_{j,y}}\psi
\]
has exactly orthonormal columns. Tracing \(Z\) gives a classical outcome. Section59's polar restoration gives legal finite approximations to this known channel, followed by separately certified realization error.

There are \(M\) fresh-pair preparations and one final readout event. Charge each total unhalved error at most \(\eta/(M+1)\), half to finite specification approximation and half to its trusted realization. The readout bound is a complete diamond bound uniform in \(y\) and the retained reference state. Additional elementary instructions require reallocating the same total pathwise budget.

Section59 gives output-index TV at most \(\eta/2\). Apply it to the original bad-output event \(d_N(E,C_j)>\delta\): actual failure is at most \(\eta\). Discontinuous risk boundaries and bad records need no continuity assumption. Returned rational centres and the decoder are unchanged.

Approximate fresh preparation remains tensor-separated from old stored references. Only completed outputs undergo collective processing. Hence the finite-control construction retains fresh single-call acquisition and the same query lower model.

### 5.5 What effectiveness does and does not establish

The computed \(M\), finite dictionary, algebraic readout table and finite trusted specifications all terminate at rational public tolerances. The table may have \(2^M\) classical strings, each an \(L\)-outcome measurement on dimension \(d^M\). Quantifier-elimination time, coefficient sizes, algebraic descriptions, quantum workspace and gate count are not bounded by query or payload optimality. No physical experiment or general high-dimensional synthesis has been executed by the finite reference checks.

## 6. R51, provenance and preserved proof credit

The current response includes all R01–R12, D01–D26 and all 32 M/P/U/V/E gates. Independent human priority remains R02/P01. The literature audit credits the existing tomography upper, coin classicalisation, standard amplification and real-algebraic decision procedures; no unspecified first-result claim is added.

The current source baseline is v79's 383 files and 759/260/116 labels. Reconstruction, ordinary/optimized finite checks and page review must bind the actual v80 source and publication objects. Their outcomes are recorded in current evidence; successful predecessor CI does not establish successor proof or execution. No human signature or journal acceptance is inferred.

The full historical A/B/C/D gates remain in the history audit, with all aggregate flags false. The complete inherited written proofs remain active or preserved at their original named paths. The following predecessor audit is reproduced verbatim.

---


### Current complete-body upper extension

The current two-construction upper is
\[
 C N^2\delta^{-2}\min\{d^2+d\log(1/\eta),\ (d^4/b)\log(d/\eta)\}.
\]
The first construction applies the all-confidence binary operator estimator at accuracy `delta/(2N)` and the hybrid inequality; it uses fresh one-call acquisition. The second is the retained cap-`b` common learner. Public parameters determine the cheaper budget. This improves the available dimension upper without identifying it with the strengthened lower or closing the joint full-body minimax problem. The common range is `d>=2`, `1<=b<=N`, `0<delta<=min(2^-13,delta_*)`, `0<eta<=1/8`.

The real and imaginary parts of the subnormalized Choi block entries are rational-coefficient polynomials. The final outcome probabilities used in Section 63 are real polynomials.

# Proof audit — Revision 79

This is an author-side proof check, not an independent external referee opinion. Current new claims are in active Section 61; earlier proof audits remain byte-preserved.

| Obligation | Argument and scope |
|---|---|
| Joint parameter dimension | Hermitian matrices form a real `d^2`-dimensional normed space. Lebesgue volumes scale as radius to `d^2`; the unknown unit-ball volume cancels in both directions. |
| Arbitrary legal covering centres | Interior packing points are pairwise at least `4delta` apart in actual `d_N`; the metric triangle prevents any radius-`delta` ball, including one centred outside the interior, from holding two. |
| Absolute range | With `s=512delta/sqrt(N)` and `delta<=2^-13`, the nonsaturated term of the dimension-free lower comparison gives `4delta`. The packing has at least `4^(d^2)` points. |
| Constructive radius and rounding | `k=ceil(sqrt(N))`, `K=ceil(128dk/delta)` and threshold `t=delta/(16k)`. Certified approximate-input error plus row-sum rounding is at most `2d/K<=delta/(64k)`. Both resulting matrices lie in the expanded fixed interior. |
| Strict selection/equality | Reject when both `tI-H` and `tI+H` are PSD, including zero eigenvalues. Accept only strict norm separation. No floating tolerance or missing singular-pivot branch is used. |
| Cardinality, without coordinate logarithm | Disjoint radius-`t/2` operator balls lie in radius-`3/8+t/2`; size at most `(1+12k/delta)^(d^2)`. Coordinate enumeration affects computation but is not transmitted. |
| Total legal decoder | Reconstruct entire dictionary; use first covering predecessor. All fixed-length indices outside list decode to `I/2`. Malformed length/schema is an input error, not a purported theorem word. |
| Randomized converse | Packing label independent of public seed. Classify from decoded effect, apply conditional Fano, data processing through private decoder randomness, then conditional Kraft bound. Worst-target expected length dominates packing-average length. |
| Randomized upper | Public seed selects empty-only code with probability eta and fixed-length index set otherwise. No target-dependent stopping or uncharged abort bit. Expected length is `(1-eta)B`. |
| Unknown-device common learner | Imported parameter-independent binary estimator returns one legal F. Spectral clipping satisfies distance to true interior E at most twice operator error by Weyl plus triangle; no noncommutative Lipschitz premise. |
| Finite classical readout | Continuous clipping, coordinate rounding with specified ties and finite dictionary selection define a Borel finite partition of the final POVM. Trusted implementation/gate synthesis is not inferred. |
| Two converses not conflated | Query lower from `dimensionlower78`; fixed-decoder payload lower from actual cover. General randomized expected-length lower separately uses Fano–Kraft. |
| Historical results | Every old section and active label retained; global endpoint logarithms and unoptimized full-body dimension factors are untouched. |

`interior_codec_check.py` tests finite exact arithmetic, equality rejection, malformed input, abort-on-incomplete behavior, small matrix grids, two complete scalar dictionaries, replay and all fixed-length words. These tests do not establish the continuum covering, statistical minimax or Fano claims, which are written proofs. No high-dimensional theorem-scale dictionary or physical learner was run.
