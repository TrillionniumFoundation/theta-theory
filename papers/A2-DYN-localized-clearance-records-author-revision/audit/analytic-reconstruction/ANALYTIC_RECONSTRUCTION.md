# Native330–332: reconstructed author proof packet

## Identity and status

This packet contains three complete English native proof sections for integration into the full A2-DYN author manuscript. It is not a separate full article, a referee report, a publication decision, a remote CI result, or a reconstruction of the bytes of an unavailable earlier scratch draft.

The operative predecessor is commit `03d651b8709d28d90aa435fc12d608ad9c945e23`, article directory `papers/A2-DYN-physical-roof-variation-author-revision`, article tree `3010c90e2363dfe1808101a3e992eb02643c28f1`. Nine exact source readbacks are retained under `inherited/`. Each was subsequently compared byte for byte with the corresponding Git object in the fixed checkout, including its actual Git blob identity. The fresh result is `evidence/SOURCE_IDENTITY_AUDIT.json`.

The complete predecessor proof chain is inherited through the full manuscript integration, not replaced by these nine selected readbacks. In particular, the physical boundary, endpoint-momentum and growth inputs used in native260, 288, 315 and 323–325 remain the inherited statements with their original assumptions and dependency scope. This packet supplies no separate expert reconstruction of those dynamical inputs.

The new proof bodies are:

| Native section | File | Principal statements |
|---|---|---|
| 330 | `330_all_label_physical_roof_variation.tex` | `thm:av-all-bv`, `cor:av-label-tests` |
| 331 | `331_return_tower_and_polynomial_likelihood.tex` | `lem:av-tower`, `lem:av-return-components`, `lem:av-kernel`, `thm:av-likelihood`, `cor:av-exact-fourier`, `cor:av-polynomial`, `cor:av-fixed-collision`, `cor:av-denominator` |
| 332 | `332_endpoint_tested_marked_roof_operator.tex` | `lem:wo-derivatives`, `thm:wo-bv`, `cor:wo-fourier` |

The current source audit resolves all 67 reference occurrences in these files and finds their 46 new labels unique against the actual inherited native article. This is a source-consistency check, not a mathematical certificate or a typesetting claim. The root integration owns the complete native build and its current build receipts.

## Unchanged physical source and observations

Every assertion concerns the original unit-speed triangular Lorentz gas on the original interval `R in [9/20,47/100]`, its actual collision map, original section, complete collision records, and original entrance probability `nu_R^* = nu|Y_R^*/c_*`, where `c_* = 91/(10000*pi)`. The full collision-area probability is `dnu = dalpha dp/(4*pi)`. No independent return or collision process is introduced.

At fixed true collision count `m`, the exact label is `(n,k)` with `k in Z^2`: the initial section is counted among occupation indices `0,...,m-1`, while membership at index `m` is tested separately. The physical roof remains in `[m*tau_-,m*tau_+]`. The only optional weight is the original `W^epsilon`, with positive `epsilon` fixed wherever its variation constant is used. Its derivatives and normalization are not suppressed.

At fixed return number `n`, the full law in331 is that of the real variables `(K_n,N_n,S_n)`, including both lattice coordinates, actual collision count, and original physical time. It is another slice of the same complete record. It does not alter the original fixed-`m` target `(k_1,k_2,n,t)` or any condition event. The analytical bandwidth is denoted `mathfrak b`; it is independent of the outer geometric parameter `B` in the original shortage problem.

## New result 330: one-copy all-label variation

The new estimate is a sum of variation norms over every actual exact label:

`sum_label TV(D p_label) <= D_all^w = D_base^w + B_sec,end + 2*B_sec,int`.

It is proved on one complete positive physical coarea source. It does not sum separate scalar bounds and then multiply by the number of labels. On each true physical word and regular section chamber, the label vector is either zero or one unit vector in the label `ell^1` space. The derivative of the scalar coarea coefficient is consequently paid once.

The boundary accounting was reconstructed as follows:

1. An internal section visit transfers mass between two label components, at `ell^1` cost at most two. This factor cannot be replaced by one.
2. An initial or terminal section membership creates or deletes one unit vector, at cost at most one. The initial occupation contribution is included in that endpoint transition; the terminal visit is not counted twice.
3. Coincident section crossings are telescoped. Artificial seams cancel before taking absolute values. Distinct physical-word endpoints remain in the complete positive sum, with no assumed cancellation between different words.
4. The actual cap, unvisited-disk and positive critical endpoint charges remain those proved in323. Visited grazing has zero coarea trace by the inherited trace theorem, not merely by collision-area nullness.

Finite independent scalar tests and the inherited exhaustion justify the summed distributional derivative. Positivity gives summed mass at most one. Compact support and nonnegativity give `2*||p||_infinity <= TV(Dp)` componentwise; the factor one half is retained in the subsequent interval argument. The standard BV translation estimate is proved by integrating the derivative measure and summing nonnegative contributions.

Bounded coefficients depending only on the exact label retain BV and a roof Fourier bound. An arbitrary Borel function of the trajectory is explicitly not claimed to preserve this BV norm.

## New result 331: actual return law and positive finite-band likelihood

### Conservative return tower

The first return is defined directly on the actual invertible, measure-preserving collision map. The proof of recurrence uses disjoint translates of the set with no future return. Applying the same argument backwards supplies the nearest past visit. The true return images partition the original section and prove invariance of the original induced probability.

The actual tower levels are disjoint. Therefore

`integral_Y r dnu = nu(union of actual tower levels) <= 1`.

Equality with one is not assumed: it would require saturation of the full collision space. The proof needs neither ergodicity nor mixing. Invariance of the induced measure gives

`E N_n <= n/c_*`, `P(N_n>L) <= n/(c_*L)`, and `E S_n <= tau_+ n/c_*`.

These are direct statements about real collision trajectories, not assumptions inferred from a finite permutation model.

### Complete law and proof-only positive restriction

The component `(k,m)` of the actual return law is exactly the inherited density `p_{n,R}(k,m,t)dt`, because the true `n`th return at collision `m` is equivalent to the original occupation and terminal-membership event. The complete law has mass one by successive recurrence.

For the proof, write the full law as `Q^L + H^L`, where `Q^L` retains `m<=L` and the positive remainder has mass `delta <= n/(c_*L)`. Neither measure is renormalized. The complete variation sum on `Q^L` is at most `D_all^1 L`. All counts remain in the final law, target event and analytical likelihood. No BV bound is claimed for the infinite return-count sum without this positive error payment.

### Exact kernel and normalization

The probability kernel is

`k(t) = (3/(8*pi))*(sin(t/4)/(t/4))^4`.

Its transform, under `hat f(s)=integral exp(i*s*t) f(t)dt`, is the compactly supported piecewise cubic

`eta(s)=1-6*s^2+6*|s|^3` for `|s|<=1/2`, and `eta(s)=2*(1-|s|)^3` for `1/2<=|s|<=1`.

The proof computes all five jumps of its third derivative: `12,-48,72,-48,12`. Four integrations by parts give the exact sine-fourth numerator. The transform is compactly supported and `C^2`; its inverse is integrable and has tail `O(|t|^-4)`. Thus the standard integrable-transform-pair inversion theorem applies with its hypotheses verified. The mass is `eta(0)=1`, the second moment is `-eta''(0)=12`, and the first absolute moment is at most `sqrt(12)`. This is a classical Fourier fact with explicit verified hypotheses, not an imported dynamical or spectral theorem.

### Positive trajectory error and arbitrary observations

For each exact label, the original roof event is empty or a union of at most `J` bounded intervals. The analytical likelihood is the convolution of that same interval indicator with the nonnegative kernel, evaluated at the original trajectory's actual roof and unchanged discrete label. It lies between zero and one.

Using full total variation, without a one-half convention, the proved errors are:

`||mu - k_b*mu||_TV <= 2*delta + kappa_ker*V_L/b`,

`E |1_A-lambda_A,b| <= delta + kappa_ker*J*V_L/b`.

The distinction between `2*delta` and `delta` is necessary: the first compares two positive measures of the same remainder mass, while the second bounds a pointwise difference of two numbers in `[0,1]` on the same trajectories. The interval symmetric difference costs at most `2*J*|h|`. The exact compact-BV height factor one half cancels that two. No lower interval width is used.

Every bounded Borel trajectory observation multiplies the second bound by its supremum norm. The selector can depend on all collisions and on the same event; no independence or selector derivative is assumed. This is why331 covers information that is outside the smooth BV test class of332.

### Exact marked transform and polynomial payment

For one exact lattice/collision label, full torus orthogonality and compact roof-frequency support give the exact four-coordinate formula with normalization `(2*pi)^(-4)` and roof factor `eta(s/b)*hat(1_I)(-s)`. The transform is that of the entire actual return law. Every torus frequency and arithmetic class is retained. A general label-dependent event is obtained as a positive sum of one-label likelihoods; no uncontrolled infinite complex label series is interchanged with the frequency integral.

For `P>0`, `kappa>=0` and `J_n<=J_0*n^kappa`, use

`L_n=ceil(n^(P+3))`, `b_n=n^(2*P+kappa+5)`.

The normalized tail exponent is `2+1-(P+3)=-P`. The normalized event-kernel exponent is `2+kappa+(P+3)-(2*P+kappa+5)=-P`. The ceiling costs at most the stated factor two. For the law error without `J_n`, the exponent is `-P-kappa`, which is no larger than `-P`.

At fixed collision count, use the original positive source `w*eta_R(T^m x)dnu_R^*`, no count restriction and no remainder. Taking `b_m=m^(P+kappa+2)` yields the original `m^2` absolute-error scale `O(m^-P)`.

All are substitutions into finite-parameter inequalities. They do not interchange the original geometric limits, alter the microscopic window, or supply a Gaussian or arithmetic peak asymptotic.

### Actual conditional denominator

For an actual information event `H`, the exact and likelihood weights are `a=1_H*1_A` and `b=1_H*lambda`. Their masses are the real selected masses `p` and `p_b`. If `E|a-b|<=E`, then `|p-p_b|<=E`. When `p>E`, the normalized measures have full variation distance at most `2*E/p`, proved by adding and subtracting `b/p`. If instead `p_b>E` is known, the valid bound is `2*E/(p_b-E)`.

Each information restriction has its own denominator. A lower bound for a larger event is not inherited by restriction. A zero arithmetic event cannot be conditioned on. No uniform denominator lower bound is invented. The result does not automatically transfer to a stationary entrance law with an unbounded return-roof weight. Nor does an absolute event error become a pointwise density error without paying the roof-window length.

## New result 332: weak endpoint-tested marked operator

### Actual derivative and norm

Tests belong to `C^1` on the compact collision cylinder, with

`||a||_C1 = ||a||_infinity + max(||partial_alpha a||_infinity,||partial_p a||_infinity)`.

Both actual partial derivatives are used. At fixed Gauss angle, `g=ze`, `H=e^T G^(-1)e`, and differentiation gives

`q_t=G^(-1)e/(z*H)`, `z_t=1/(z*H)`.

The factor `H` is essential. The exact first variation `g=R(-p_0,p_m)` supplies the endpoint momentum derivatives. Together with the Hessian bounds, this yields the endpoint-test constant

`C_test,end = Lambda_circ*(lambda_circ^(-1)+R_-^(-1))`.

Its name is deliberately distinct from the radius-disintegration constant `C_end` already used in inherited296.

### Interior observations without inverse incidence

The actual momentum is differentiated as a geometric tangential component:

`p_i=v_i dot n'(alpha_i)`,

with the incoming terminal velocity at index `m`, since reflection preserves the tangential component. Therefore

`|D p_i| <= ||D v_i|| + |D alpha_i|`.

The inherited unweighted endpoint Jacobi estimate and the real-flight lower bound imply `|D p_i[eta]|<=C_c*s_i*||eta||_infinity` without a denominator `c_i`. This differentiates neither `sqrt(1-c_i^2)` nor the forward map with fixed initial momentum. The difference from the expanding forward-orbit derivative is explicit in the theorem and its scope paragraph.

For a real phase `Psi_m=sum phi_i(T^i x)`, put `l_i=max(sup|partial_alpha phi_i|,sup|partial_p phi_i|)` and `L_m=sum l_i*s_i`. Then

`z*|partial_t Psi_m| <= C_test,phase*L_m`,

`C_test,phase=(Lambda_circ/lambda_circ)*(J_*+C_c)`.

The exact geometric sum `sum_{i=0}^m s_i=2*(1-sigma^(m+1))/(1-sigma)` is bounded uniformly in the full collision count. If all `l_i<=L`, then `L_m<=2*L/(1-sigma)`. All physical collisions remain observed.

### Full inverse-gradient payment and boundary accounting

The complete additional interior cost is paid using

`integral_theta sum_word integral A/z dt = c_*^(-1)*integral_cap 1/z dnu <= J_cross/c_*`.

The inequality uses `I_m>=1` and the full physical multiplier theorem315. It includes every actual word and near-critical positive bulk. It contains one conditioning division. Inserting the separately conditioned multiplier estimate and then dividing by `c_*` again would be a different normalization and is not done.

The bounded test multiplier multiplies the inherited complete physical endpoint charges. Positive critical traces remain positive charges. Visited-grazing traces remain zero because the actual coarea coefficient tends to zero, even if the gradient also tends to zero. Interior and endpoint section jumps retain costs two and one. The guard derivative is paid once in `D_base^w`; it is not added again to the new test derivative.

The resulting all-label variation bound is

`sum_label TV(D f_label) <= D_all^w*a0*b0 + J_test*[C_test,end*(a1*b0+a0*b1)+C_test,phase*L_m*a0*b0]`,

with `J_test=J_cross/c_*`, and the summed `L1` norm is at most `a0*b0`.

### Operator strength and remaining closure

Summing the true label characters and integrating the compactly supported BV roof density by parts gives a bounded map from the stated `C^1` space to its complex linear dual:

`||K_m,R(s)|| <= min(1,(D_all^w+2*J_test*C_test,end)/|s|)`.

The optional chain phase adds `J_test*C_test,phase*L_m` to the numerator. The bound is uniform in the actual radius, collision count and real mark frequencies.

This is a weak endpoint-tested roof estimate. It proves no strong anisotropic transfer-operator estimate, no iteration-compatible strong norm, and no decay in the return or collision count. Its `1/|s|` tail is not integrable at infinity. Consequently it does not by itself justify absolute Fourier inversion over an expanding domain, the uniform arithmetic peak expansion, the raw pointwise local theorem, or the long-time four-coordinate inverse Jacobian bound.

The original endpoint-layer shortage and the remaining spectral/local-limit closure retain their original physical events, normalizations, suprema and ordered limits. Their precise remaining mechanisms belong to the full proof ledger. None is silently replaced by a weaker averaged theorem, a wide window, or one of the finite checks below.

## Fresh exact validation and its limits

The two entry points are `check_all_label_likelihood.py` and `check_marked_weak_operator.py`. Their only shared local module is `analytic_check_support.py`. Each accepts `--details`, `--source-root`, and `--output`. The default source resolver handles both this packet and the integrated article's `core/` and `scripts/` layout.

The checks use exact `fractions.Fraction` arithmetic and finite polynomial identities, with explicit exceptions for failure. Python optimization removes none of them. Each output binds the current native bodies, current program and helper, and eight unchanged inherited mathematical inputs by SHA256; the inherited files must match their fixed expected hashes before a successful result can be emitted.

| Entry point | Checks per execution | Groups | Actual executions | Determinism |
|---|---:|---:|---:|---|
| `check_all_label_likelihood.py` | 74,071 | 34 | normal and `-O`, both exit 0 | complete JSON outputs byte-identical |
| `check_marked_weak_operator.py` | 28,382 | 27 | normal and `-O`, both exit 0 | complete JSON outputs byte-identical |

The first checks finite label-vector transitions, BV step functions, exact finite tower identities, kernel polynomial derivatives and normalization, interval symmetric-difference payments, polynomial exponents and real conditional-denominator algebra. Its 4,129 finite permutation/section instances illustrate only the combinatorial tower identity; the native proof proves recurrence directly on the actual physical system. The second checks rational positive-definite Gauss identities, the exact inherited constants, full geometric sums, the tangential momentum differential, specified test-norm product payments, one-copy conditioning and finite BV Fourier identities.

These scripts do not certify the continuous geometry, the inherited dynamical proof chain, all collision words, the singular boundary exhaustion, a spectral gap, a raw local limit theorem, or an inverse theorem. Their purpose is to expose algebraic, normalization, sign and exponent errors in the written proofs. Their scope limits appear in the actual outputs.

`evidence/COMMAND_RECEIPTS.json` records the four commands and returned exit codes. `evidence/DETERMINISM_RECEIPT.json` records their two byte comparisons and output hashes. The two normal-output SHA256 values are:

- 330–331: `072c4608ae229a71d570cffd9ed31752fdefcb16e5313c39c40db7d01d77bf8b`.
- 332: `0a8e55ee54d5fc34739fd16bf220c14cb8df1ab41428482917129f584a4173cb`.

The same values apply to the optimized outputs. These are fresh local checks on the current reconstruction. They do not report the total full-manuscript driver count and do not report any remote CI completion.

## Corrections and historical retention within this packet

All pre-correction proof bytes were retained before changing them:

- `audit/pre-correction/` preserves the initial complete330–332 bodies and records the missing backslash before `quad` in331 and the replacement of informal glued source numbers by actual theorem references.
- `audit/pre-constant-disambiguation/` preserves332 before `C_end` and `C_phase` were renamed to the distinct test constants. No value changed.
- `audit/pre-layout-correction/` preserves331 before its exact-label likelihood definition was put in display form. The root's full-manuscript preflight identified an overfull inline box; the formula itself was unchanged.
- `audit/pre-layout-correction/execution/` preserves the two successful local outputs produced before that last source change. They are not substituted for the final source-bound outputs.
- `inherited/` preserves the nine exact readbacks and their retrieval manifest, with the additional Git-object verification in the current evidence directory.

The core proof and checker files are now frozen. The handoff manifest records their current bytes and all audit/evidence files. Earlier lost scratch hashes, manuscript page counts and command results are not reused as evidence for these bytes. The parent reconstruction owns the broader incident record, full historical manuscript preservation, independent review identity, complete article compilation, Git commit and remote publication status.
