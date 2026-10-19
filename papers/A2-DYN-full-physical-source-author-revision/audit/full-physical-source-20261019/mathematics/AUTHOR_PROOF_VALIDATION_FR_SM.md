# Author validation of the full-source roof and mixed singularity proofs

This is an author proof-validation record. It is not a new referee report and does not certify the final raw pointwise local limit theorem.

## Exact new proof sources

| Native draft | SHA256 at this validation |
| --- | --- |
| `full_physical_source_roof_regularity.tex` | `6b9fb717b942824464cd9c66be1b426ec8fb0956e895063aa764f23ebd158af2` |
| `full_physical_singular_multiplier.tex` | `07f849b3cf160e0a99248594d49ae24bee0f39986a163f6f2bc33cd18ad5da14` |

All drafting took place under `iteration-20261019b/math`. The preceding complete physical-tube article and its proof bodies were read without modification. In particular, the momentum-fibre construction and complete endpoint kernel in native module 284 were identified as already proved and inherited; they are not claimed as new in this iteration.

## 1. Quantitative exhaustion of all physical margins

The fixed-margin atlas bounds an original full-roof density by `mathfrak A epsilon^-2`. The unconditioned complement of the same class has mass at most

`[2/(R_minus(1-r_g))] epsilon + [2r_g²/(1-r_g²)] epsilon²`.

The first term follows from the exact clearance flux in 270, evaluated on every complete physical flight. The second follows from the invariant incidence marginal. The original endpoint cap implies `c_0,c_m >= sqrt(11)/6`, so only interior contacts contribute incidence failures. There are at most two contacts or flights at each depth; the respective sums start at one and zero. The chosen upper margin `1/200` is strictly inside the actual clearance-flux range `3/200`. It is an auxiliary upper bound for the proof, not a change to the microscopic event.

At each finite collision count, the positive decomposition gives

`mu(S) <= A_E epsilon^-2 |S| + B_sharp epsilon`

for every Borel roof set. Null sets first prove absolute continuity of the entire source. For high density levels, `epsilon=sqrt(2A_E/lambda)` puts the bounded part below `lambda/2`; the complementary mass gives a `lambda^-3/2` tail. For lower levels, the original subprobability mass supplies the needed bound. Thus no small or large roof set is omitted. The resulting weak `L^(3/2)` statement includes every positive physical margin and all words, but does not assert `L^infinity` control.

The original conditional measure is used throughout. Its density relative to unconditioned collision probability is `1_Y/c_*`, so the complement has precisely one conditioning factor. The atlas constant already contains its separate, single `c_*^-1` from coarea; these contributions are added in the positive decomposition and are not multiplied into an invented second conditioning.

## 2. The actual linear incidence insertion

For any physical selector `0<=h<=1` of unconditioned mass `a`, the exact incidence tail and layer cake give

`integral h/c_i dnu <= 2 sqrt(a)`.

The actual weights satisfy `sum_i q0^d_i <= 47/3`, hence

`integral h I_m dnu <= (97/3) sqrt(a)`.

No conditional independence from the roof is used. For a roof preimage, `a=c_* mu(S)`, giving the exact conditional factor `c_*^-1/2`. Combined with full roof concentration, this yields the complete actual `I_m`-weighted weak `L^(6/5)` density. The multiplier remains `1+sum q0^d_i/c_i`, with `q0=47/53` and the original collision indices.

## 3. The new mixed physical singularity mechanism

Let `r=|(p_0,p_m)|`. Integrating the complete inherited kernel 284 without an initial section factor gives, on the same actual physical source,

`nu{r<s} <= A_0 s²`, with `A_0=C_mom/4`.

Applying that kernel to the actual prefix block ending at collision `i` gives

`nu{r<s,c_i<u} <= A_1 s u²`, with `A_1=C_mom/pi`.

This second estimate is a joint-density area bound under `(p_0,p_i)`, after the inclusion `r<s => |p_0|<s`. It is not multiplication of marginal probabilities. Both inequalities hold for all positive `s,u`: for `u>=1` the complete momentum interval has length two, which is bounded by `2u²`. This removes any hidden threshold restriction in the subsequent tail argument.

For `X_i=1/(r c_i)`, splitting into `r<b` and the complete annuli `2^j b<=r<2^(j+1)b` gives

`nu{X_i>t} <= A_0 b² + 4A_1/(t² b)`.

The substitution `b=(A_1/A_0)^(1/3)t^(-2/3)` yields the exact valid coefficient

`K_cross=5A_0^(1/3)A_1^(2/3)`

in a uniform `t^(-4/3)` bound. Layer cake then gives the restricted integral `4K_cross^(3/4)a^(1/4)`. Summing the true incidence weights and including the unmarked inverse-gradient term proves

`integral h I_m/|grad_q F| dnu <= J_cross a^(1/4)`,

where

`J_cross=R_minus^-1 [2sqrt(A_0)+(188/3)K_cross^(3/4)]`.

The physical first variation is exactly `|grad_q F|=Rr`; the radius factor is retained. This proves a uniform complete bulk first moment, weak `L^(4/3)` physical distribution, and strong physical moments below `4/3`. Separate weak `L²` marginal tails would not prove this result. The validation program contains a rigorous abstract counterexample to that invalid inference and explicitly identifies it as a nonphysical analytical control.

The original conditional form is `J_cross c_*^(-3/4) mu(S)^(1/4)`. This follows by substituting `a=c_*mu(S)` before division by `c_*`; it is not a guessed normalization.

## 4. Original critical bands and regular-interior variation

The inherited Borel critical-origin band 286 gives the actual containment `r<=A_s=min(rho,sqrt(2U_m s))`. The new joint estimate implies

`integral_{r<a} 1/c_i dnu <= 2sqrt(A_0 A_1)a^(3/2)`,

`integral_{r<a} 1/(r c_i) dnu <= 6sqrt(A_0 A_1)a^(1/2)`.

Consequently the complete actual `I_m/|grad F|` volume in such a band is bounded by

`[2A_0 A_s+94sqrt(A_0 A_1)sqrt(A_s)]/(c_*R_minus)`.

The resulting `O(s^(1/4))` estimate contains the actual incidence insertion absent from the prior 286 estimate. Shorter arms contribute only their actual points. No arm is continued through a third disk or section boundary, and no arbitrary endpoint trace is dominated by a bulk measure.

The regular-interior variation corollary uses precisely the already proved 289 inequality and the retained one-copy coarea identification. The physical selector is multiplied after differentiating `f^epsilon`; neither it nor a section, roof or exact-label indicator is differentiated. The complete sum of these derivative measures is now finite. On the exact deep exceptional source its `m²`-normalized total variation vanishes. Jumps between distinct physical segments and independently defined singular paired traces remain separate.

## 5. Rates, exact marks, and remaining limits

For the actual exceptional union 309 at `D_m=ceil(theta m)`, the six-term 312 saturation budget has rate `exp(-lambda_b m)`. Its squared-incidence coefficient 16 remains intact. The three complete roof densities have the following weak endpoints and mass rates:

| Actual source weight | Roof weak space | Weak norm rate | Total mass rate |
| --- | --- | --- | --- |
| `1` | `L^(3/2,infinity)` | `exp(-lambda_b m/3)` | `exp(-lambda_b m)` |
| `I_m` | `L^(6/5,infinity)` | `exp(-lambda_b m/6)` | `exp(-lambda_b m/2)` |
| `I_m/|grad F|` | `L^(12/11,infinity)` | `exp(-lambda_b m/12)` | `exp(-lambda_b m/4)` |

Strong roof norms below these endpoints have respective exponents `2/p-1`, `2/p-3/2`, and `2/p-7/4`. These are positive on their specified ranges; the strong endpoint norms are not claimed. Every resulting positive exponential rate dominates the original `m²` factor. All physical sums precede the radius and label suprema. The auxiliary finite-count margin optimization does not exchange the original collision limsup with outer `B` or its microscopic windows.

The full-source marked Fourier comparison retains the exact central integer observations and the actual clock identity. Its compensating phase is `exp(-isW_d)`, leaving only the nonnegative transport clock error. The applicable integer range is `d>=1,2d<m`. The same proof now includes the actual singular multiplier. It controls the stated bounded, exponentially growing roof-frequency range; it is not an unbounded Fourier integral.

The original raw pointwise goal remains open. A density can have exponentially small weak norms on an exponentially short roof set while retaining nonzero normalized essential height. The new full bulk singular estimate therefore completes an actual source budget, but does not erase the original shallow positive source, arbitrary boundary traces, full comparison capacity or remaining spectral/arithmetic/conditional interfaces.

## Actual auxiliary executions

Program: `check_full_physical_source.py`, SHA256

`5ce165494294167ac2215a798f621f4a1ab6e5f2cd396d0dcce7c76846f4a3ca`.

The program uses explicit error gates rather than Python `assert`. Its `--details` output is deterministic. Normal and `-O` executions both exited zero between `2026-10-19T08:01:48Z` and `2026-10-19T08:01:51Z`; both stderr files are empty. Both stdout files and both details files have SHA256

`9a1c4809877658b3ce813c43c48612f1b0261335f101e3f5b7fe1ffcf6dfc33e`.

The complete commands, times and output hashes are preserved in
`verification-full-source/20261019T080148072679Z/RUN_RECEIPT.json`.

The checks include exact symbolic identities, all relevant normalization and exponent transitions, 512 finite collision-count depth audits, all-level dyadic algebra, the original Fourier sign, and analytical negative controls. The continuous physical kernel, atlas and coarea arguments are native mathematical proofs; a finite program is not their replacement. Build, publication and remote CI status belong to their separate actual execution records.
