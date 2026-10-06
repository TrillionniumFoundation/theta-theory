# Proof and resource audit — Revision 87

This is an author-side audit of written proofs. It is neither a proof-assistant certificate nor independent specialist priority clearance. The controlling R56 report bytes and all predecessor proof sections are unchanged.

## 1. Nonemptiness with explicit parameters

Choose a>0 bounding all component operator norms of H and lambda>0 below every positive effect eigenvalue on its support. Zero effects are handled separately, with H_j positive. For s<=min(1,lambda/(2a),1/a), the support block of E_j+sH_j+cs²I is at least lambda/2. The cross block is sP_jH_jQ_j, and its Schur correction is at most 2a²s²/lambda. Taking c=1+2a²/lambda proves positivity even with a singular opening block. The common denominator 1+kcs² is positive for all real s and normalizes exactly.

The exact remainder, not a formal expansion, is `cs²(I-kE_j-ksH_j)/(1+kcs²)`. Since each effect has norm at most one and sa<=1, its norm is at most c(1+2k)s². Summing gives Lambda*=ck(1+2k). This guarantees one member at every scale in the interval for any allowance at least Lambda*. It does not decide the optimal allowance or show infeasibility for smaller ones.

On Gaussian-rational input, rational support projectors are obtained by the existing exact support routine. A rational real-plus-imaginary row-sum majorant gives a>=1. Repeated halving of lambda from one ends after polynomially many steps by rational-matrix nonzero-eigenvalue bounds; each step uses a full exact PSD test. The implementation rejects an exhausted cap. The certificate certifies the whole displayed rational curve by these hypotheses and the analytic proof, not by its sampled checks. Rational in the parameter and rational in all coefficients are distinguished.

## 2. Precise acquisition class

A block is a complete probe–reference group, with at most b inputs to the unknown channel. Different groups are initially independent. Entanglement within a group and arbitrary reference dimension are allowed. Public mixtures and partitions have a retained classical record; no channel output changes any input. An arbitrary final joint readout is allowed.

At b=1 this is the prior product-reference model. At b=N it is the full parallel diamond norm of the difference of tensor channel powers. Padding with discarded calls handles smaller budgets. Shared quantum reference correlations between otherwise separated groups are not included by this definition. We do not claim to classify every classical-feedback or separable-probe-with-shared-reference model.

## 3. Finite Bures upper for entangled blocks

For a tangential direction with Q_jH_jQ_j=0, use the canonical normalized factor, not the horizontal solution. Write beta0=||B||op, K=k beta0²(2+h), r=Lambda+K. The factor displacement is at most 3 beta0 s/2. Tensor telescoping on an arbitrary n-call input and reference bounds its purified displacement by 3 beta0 n s/2. This controls the Bures distance of base and surrogate outputs.

The finite tube/surrogate channel error is at most rs² per call, hence nrs² for the whole block. The Bures distance to the actual F output is at most s sqrt(nr). Add these by the Bures triangle inequality. Before the final readout, the outputs of different blocks are products, so their root fidelities multiply. Their squared Bures distance is bounded by the sum of squared block Bures distances. Unhalved trace norm is at most twice Bures distance. This gives the exact displayed finite upper before using sum n_r²<=bN.

No product-state assertion is made inside a block; its input may be arbitrarily entangled. Common-weight direct sums handle retained public randomization. Both the unknown-remainder term and the reference dimension are controlled explicitly.

## 4. Parallel lower, rather than sequential input adaptation

The inherited one-call corrected channel has Phi_E=Id and diamond error at most kappa s² from the logical unitary, with kappa=Lambda+2||Gamma||op². This holds uniformly over the allowed remainder by the finite tube proof, not by a rank-regularity assumption. The completed recovery acts on the actual classical label and retained reference only.

Prepare a GHZ state on m logical qubits and apply the tensor encoding before any call. After all m calls, tensor the local recoveries. The resulting channel is Phi_F tensor m, not its m-fold composition. Channel tensor telescoping gives m kappa s². The ideal phase difference on the GHZ span is msDelta. Trace norm therefore has the finite lower `(2|sin(msDelta/2)|-m kappa s²)_+`.

For amplification across independent blocks, use a signed Pauli-Y observable on the GHZ span, zero off the span. The effect (I+Y)/2 is globally legal. Its base probability is 1/2; its alternative differs from 1/2+sin(msDelta)/2 by at most m kappa s²/2. This last factor is the event bound for the difference of normalized states. The preparation and readout depend on E,H,s,m, not the unknown tube remainder. References have dimension at most 2d per call. This is not a polynomial circuit-size guarantee.

## 5. Uniformity in N and block width b

Decrease the fixed scale interval so that sDelta<=1/4 and kappa s/Delta<=1/pi, in addition to the inherited interval. Set m=min(b,floor(1/(2Delta s))) and ell=floor(N/m). Then 1<=m<=b, ell>=N/(2m), and x=mDelta s<=1/2. The binary alternative gap is at least x/pi - (kappa s/(2Delta))x >=x/(2pi). Repeat ell independent blocks and use the fully finite Bernoulli lemma.

If m=b, sqrt(ell)x>=Delta s sqrt(Nb/2). If m<b, floor arithmetic gives x>=1/4, and the finite Bernoulli lower is at least 1/(1024pi). Both cases bound a fixed multiple of min(1,s sqrt(Nb)), with constants independent of N,b,F. The construction uses at most ell*m<=N calls on every record. No large-block limit is taken before paying the remainder.

The regular row follows by sandwiching between the old product lower and adaptive upper; the latter retains `2 beta_h sqrt(N)s+(Lambda+K_h)Ns²` before truncation. The opening row follows from a fixed impossible-event product lower and the old hybrid adaptive upper. These proofs keep the two linear mechanisms distinct.

At b=N the width result and adaptive tube theorem have matching local orders. There is no assertion of equality of exact distances, perfect discrimination or fixed-pair asymptotic error exponents. In particular the published adaptive-versus-parallel separations for other channel pairs are not contradicted.

## 6. Higher-order and computational scope

The power corollary substitutes s=t^q under the actual finite remainder <=Lambda t^(2q). It does not differentiate an inverse parameter and does not classify a general zero first jet. The mixed scalar family remains an explicit example of an intervening scale.

The executable decides the represented cone branch and reports the proven resource orders, then supplies a sufficient rational nonemptiness certificate and optional supplied-pair check. It does not evaluate the adaptive distance, construct the support code, synthesize a recovery, certify approximate controls, or compute the discrimination scale interval. It labels zero tangent `higher_order_undetermined`.

## 7. Exact finite scope and negative controls

The new suite executes 591 checks and 21 rejection controls. Twelve complete qubit GHZ probability laws use m=1,2,3,4 and rational rotations s=1/8,1/16,1/32. All 2^m outcome strings are computed by exact Kronecker effects. The probabilities match the closed parity formula and their complete l1 separation equals the parity signal. This checks a concrete entangled parallel input, not an inferred general recovery implementation.

Additional tests cover explicit nonempty realizations with zero effects and singular cross-support openings, finite remainder budgets, rational support floors, tensor error inequalities, all integer compositions through six calls, and 42 block-allocation plans. Mutations of the support floor, scaling, minimality, dimensions, rational format, nonempty interval, supplied pair, or execution claims are rejected. Normal and optimized Python results must agree. The 24 old suites remain active and execute again; no old success is reused as current evidence.

Finite tests do not prove the continuum theorem. The role of GHZ, fidelity, the semidefinite cone and the QEC/metrology criterion is explicitly credited. The new theorem is their finite effect-tube synthesis with a uniform block-width tradeoff.

## 8. Preservation and independent pipeline

The 600-file v86 native inventory is preserved. All mathematical sections are byte-identical relative to v86, with no new insertion or deletion. All active complete, quantitative-plus-supplement and structural label sets remain. Original changed entry/audit/build files are retained under predecessor-v86-audit. Source, publication and exact final review identity must have separate fresh receipts.

The full historical A/B/C/D chain remains independent. Measurement discrimination and coding do not establish raw local limits, path LDP recovery, a global past kernel, shell conditioning, process CLT/Mosco, nonlinear graph cores, filtering/QMD/LAN, changing-filtration response or labelled posterior contraction. All five aggregate flags remain false.
