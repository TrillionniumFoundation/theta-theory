# Written-proof audit — Revision 77

This is an author-side audit of the written theorem chain and its revision interfaces. The controlling external materials are `FROZEN_R50_REPORT.md` and `FROZEN_R50_PIPELINE_AUDIT.md`, which review the completed v76 object at `c041c011274973728a8cc55029192c057696aa43`. The predecessor proof audit is preserved in `predecessor-v76-audit/PROOF_AUDIT.md`. The mathematical details retained below document the inherited arguments; the v77 audit concentrates on the first-rejection learner specification, the arbitrary-dimensional learning extension, the deterministic matrix code, and their compatibility with those arguments.

Separate internal agents cross-read the qubit procedure, endpoint calibration, harmonic-mean comparison, compression, matrix assembly, and coding construction. This is internal mathematical cross-review, not an independent human referee opinion, proof-assistant certificate, human priority clearance, or authorship attestation. Preservation of inherited full proofs is not represented as a new independent review of every historical theorem. `RESPONSE_TO_REFEREE.md` records the r50 dispositions; Section 13 below lists all D01–D36 technical checks.

## 1. The new statements and their different scopes

| Statement | Mathematical object | Quantifiers and resource |
|---|---|---|
| `thm:matrixmetric76` | The complete ordered binary effect body on `C^d` | Every finite `d`, every integer `N>=1`, every pair, all support ranks and multiplicities; comparison constants depend on `d`. |
| `lem:matrixball76` | Actual operational balls in that body | Uniform two-sided measure bounds at all centres for sufficiently small radii, with dimension-dependent constants. |
| `thm:matrixcover76` | The same complete body | Fixed `d`, all `N>=1`, `0<delta<=delta_d`; arbitrary legal memoryless centres in the converse; full matrix entropy including every support rank and spectral multiplicity. |
| `thm:commonlearn76` | The complete ordered binary **qubit** body | One common learner, uniform failure at most `eta`, sufficiently small `delta`, `0<eta<=1/8`; training calls of order `N delta^-2 log(1/eta)`, where `N` is the future loss horizon. |
| `thm:matrixlearning77` | The complete ordered binary body in every input dimension | Every `d,N>=1`, absolute small-error cap, `0<eta<=1/8`; `C d^4 N delta^-2 log(d/eta)` calls on every record and a scalar lower bound `cN delta^-2 log(1/eta)`. The order is matched at fixed `d`, not in growing `d`. |
| `thm:matrixcodec77` | Supplied Gaussian-rational matrix effects | Finite exact deterministic encoder and decoder for rational `0<delta<=1`; radius at most `11delta/16`; optimal payload order in the separately stated small-error range. |
| `cor:matrixlearnedcode77` | An unknown matrix-effect device followed by rational postprocessing | Common future-loss learning followed by deterministic encoding, with no additional device calls or statistical failure allowance. |
| `thm:biasedcodec75` | Rational Cartesian qubit effects | Implemented exact encoder and legal decoder; one charged index; target approximation from the written construction and canonical replay. |

The device has two ordered outcomes, consumes its input, and supplies no residual quantum output. The arbitrary-dimensional results concern the entire Hermitian effect interval, including all ranks and multiplicities. The qubit learner remains an explicit subroutine; Sections 56 and 57 add a common learner and a finite exact codec on the full matrix body. In the inherited qubit codec, `dimension` equal to two or three counts Bloch coordinates, not the Hilbert input dimension `d` used by the matrix tools. No theorem here asserts a multiple-outcome or disturbing-instrument extension.

## 2. Operational normalization and intrinsic matrix form

The target is

\[
 \mathfrak E_d=\{E=E^*\in M_d(\mathbb C):0\preceq E\preceq I_d\},
\]

with ordered effects `E,I_d-E`. The distance `d_N` is the supremum of the unhalved output trace norm over common reference-assisted adaptive testers with at most `N` calls and bounded public stopping. The nonadaptive restriction permits input entanglement and a retained reference. A lower witness may depend on the known pair but not on the unknown choice within that pair.

For one call the difference has reference blocks `B_rho,-B_rho`, where

\[
 B_\rho=\operatorname{tr}_{\rm in}[((E-F)\otimes I)\rho].
\]

Duality against Hermitian contractions bounds `||B_rho||_1` by `||E-F||op`. An extremal eigenstate of `E-F` attains that bound. Thus

\[
 d_1(E,F)=2\|E-F\|_{\rm op}.
\]

The same argument inserted slot by slot gives the hybrid inequality `d_N(E,F)<=2N||E-F||op`. It proves continuity at fixed `N` and allows boundary limits and rational approximation. Classical transcript total variation remains half the corresponding trace norm.

For `tau=1/N`, define `V_G=G(I_d-G)` and the positive operator

\[
 \mathcal A_G(H)=V_GH+HV_G+\tau H
\]

on the real Hilbert space of Hermitian matrices. Its eigenvalue in the matrix-entry direction `(i,j)` is `v_i+v_j+tau>0`. The form

\[
 g_{N,G}(H)^2=N\langle H,\mathcal A_G^{-1}(H)\rangle_{\rm HS}
\]

therefore exists on the entire closed body. For `M=(E+F)/2` and `H=F-E`, the comparison modulus is `Q_N(E,F)=g_{N,M}(H)`. At repeated eigenvalues it is intrinsic: different eigenbases represent the same positive superoperator and quadratic form. No triangle inequality for `Q_N` is used. Every packing and covering argument uses the genuine operational metric `d_N`.

## 3. The horizontal dilation and the adaptive path bound

### 3.1 Realizing the tangent by exact measurement factors

At an interior effect `G`, put `S=sqrt(G(I_d-G))`. For Hermitian `K`, prescribe the tangent `H_0=SK+KS` and choose

\[
 A_1=\sqrt G,\quad A_0=\sqrt{I_d-G},\qquad
 B_1=\sqrt{I_d-G}\,K,\quad B_0=-\sqrt G\,K.
\]

Direct multiplication gives

\[
 A_1^*B_1+B_1^*A_1=H_0,\qquad
 A_0^*B_0+B_0^*A_0=-H_0,
\]

and the two crucial identities

\[
 \sum_y A_y^*B_y=0,\qquad\sum_y B_y^*B_y=K^2.
\]

These are realized by genuine nearby dilations. Let `R_y(s)` be the positive square root of the exact effect `G+sH_0` or its complement. Set

\[
 T_y=(B_y-R_y'(0))R_y(0)^{-1}.
\]

Multiplying `T_y+T_y*` on the left and right by `R_y(0)` gives zero by differentiating the effect identity. Hence `T_y` is anti-Hermitian. The factor `exp(sT_y)R_y(s)` has exactly the desired effect and derivative `B_y`. The rotation acts on the discarded factor environment. The output channel, including its action on a retained input reference, remains the required classical-output measurement.

The measurement isometry keeps one copy of the outcome in the observed register and one in its environment. Its derivative obeys

\[
 W^*\dot W=0,\qquad\dot W^*\dot W=K^2.
\]

The first identity is operator-valued on the input space, which is essential for adaptive use with arbitrary memories.

### 3.2 Orthogonality through an arbitrary common tester

Fix and purify a tester and all its intervening operations. The derivative of its final purification is the sum of `N` vectors, each containing one differentiated channel slot. For two different slots, cancel the common isometries after the later slot. The remaining cross term contains `W* dot W tensor I=0`. Thus the derivative vectors are mutually orthogonal even when the earlier inputs are entangled with the memory and depend on previous outcomes.

Each vector has norm at most `||K||op`, so the derivative of the final purification has norm at most `sqrt(N)||K||op`. The pure-state trace-norm derivative and contraction under the environment trace give an observed derivative bound `2sqrt(N)||K||op`. Public stopping is handled by padding with fixed dummy inputs and discarded outputs. The purification retains the auxiliary environments for analysis only; the tester does not gain access to them.

### 3.3 The regularized Sylvester split

For an arbitrary Hermitian tangent `H`, solve

\[
 SK+KS+N^{-1/2}K=H.
\]

The solution is unique and Hermitian. Write `H=H_0+R`, with `H_0=SK+KS` and `R=N^-1/2 K`. At an interior effect these are legitimate tangents. The derivative of a fixed tester's output is linear in the inserted channel tangent. The horizontal part costs at most `2sqrt(N)||K||op`; the remainder costs at most `2N||R||op` by the one-call duality and the hybrid insertion argument. This is a split of the differential, not a claim that the path is a physical mixture of two channels.

In an eigenbasis of `G`,

\[
 K_{ij}=\frac{H_{ij}}{\sqrt{v_i}+\sqrt{v_j}+N^{-1/2}}.
\]

The squared denominator is at least `v_i+v_j+N^-1`, so

\[
 \sqrt N\|K\|_{\rm op}\le\sqrt N\|K\|_{\rm HS}
 \le g_{N,G}(H).
\]

Integrating the derivative bound for each fixed tester, and taking the supremum afterwards, gives

\[
 d_N(G(0),G(1))\le4\int_0^1g_{N,G(t)}(G'(t))\,dt.
\]

No interchange of a supremum and a derivative is required. For a boundary path, replace it by `(1-2epsilon)G+epsilon I`, apply the interior argument, and let `epsilon` decrease to zero. The fixed-horizon form is continuous and bounded by `N||G'||HS`; the hybrid inequality gives endpoint continuity. Lemma `lem:matrixpath76` therefore includes the closed body.

### 3.4 Straight segments and the constant eight

The map `G -> G-G^2` is operator concave. Along the segment from `E` to `F`, with midpoint `M`,

\[
 V_{G(t)}\succeq 2\min(t,1-t)V_M.
\]

This order passes to the sum of left and right multiplication: its quadratic-form difference at a Hermitian `X` is `2 tr((V_G-aV_M)X^2)>=0`. The cutoff also dominates its multiple by `a=2min(t,1-t)<=1`. Inversion reverses the order of positive operators, hence

\[
 g_{N,G(t)}(H)\le[2\min(t,1-t)]^{-1/2}Q_N(E,F).
\]

The scalar factor has integral two. The path bound therefore gives `d_N<=8Q_N`, and the trace-norm cap gives `d_N<=min(2,8Q_N)`. The endpoint singularity in this comparison is integrable and does not require a positive spectral margin.

## 4. Matching nonadaptive lower witnesses

In an eigenbasis of `M`, put

\[
 q_{ij}=|H_{ij}|\sqrt{\frac N{v_i+v_j+N^{-1}}},
 \qquad Q_N^2=\sum_{i,j}q_{ij}^2.
\]

For a diagonal entry, repeatedly use the corresponding eigenvector of `M`. The Bernoulli parameters are `m_i-H_ii/2` and `m_i+H_ii/2`. Their maximum variance is at most the sum of their variances, which is at most `2m_i(1-m_i)`. The preserved Bernoulli lemma therefore gives `d_N^na>=min(1,q_ii)/64`, including parameters zero and one.

For an off-diagonal entry, restrict each input to the span of the two corresponding eigenvectors. The induced channel has exactly the compressed binary effects, also on entangled inputs. Variances in the following argument are formed from those compressed matrices. Their exact midpoint identity gives

\[
 v_i+v_j+N^{-1}
 \ge\tfrac12(V_E^{\mathcal S}+N^{-1}),\qquad
 v_i+v_j+N^{-1}
 \ge\tfrac12(V_F^{\mathcal S}+N^{-1}).
\]

For their qubit spectral gaps `r,r'` and directions `u,v`, the traceless part of their difference has norm `|ru-r'v|/2`. Its off-diagonal entry is bounded by

\[
 \frac12\bigl(|p-p'|+|q-q'|+\min(r,r')h\bigr).
\]

Together with the variance identity, this bounds `q_ij` by `1/sqrt(2)` times the preserved qubit spectral/angular comparator. If one gap vanishes, the angular term is zero and no direction is chosen for the scalar effect. The nonadaptive qubit comparison then yields `d_N^na>=min(1,q_ij)/8192` for the original pair by a fixed isometric embedding.

At least one entry has `q_ij>=Q_N/d`. Taking the strongest of the separate experiments proves

\[
 d_N^{\rm na}\ge\frac1{8192d}\min(1,Q_N).
\]

This use of a maximum requires no common state that extracts all entries. Combining the upper and lower bounds gives `cor:matrixadaptivity76`; the identical pair is handled without division, and the trace-norm cap gives the claimed factor also when `Q_N>=1`.

The separate spectral lemma uses the nonzero intersection of the first `k` eigenspaces of `E` and the complement of the first `k-1` eigenspaces of `F`. A vector in this intersection orders its two Bernoulli probabilities outside the two ordered eigenvalues. Bernoulli stochastic monotonicity then gives the desired lower bound for that eigenvalue. Multiplicities cause no failure of the dimension argument. In a common ordered eigenbasis, `N` Bernoulli bits in each of `d` rows form a reference-compatible common programme and give an upper sum of row distances. This is an upper bound, not an asserted exact product-distance formula for arbitrary commuting pairs.

## 5. Local forms and actual operational-ball volume

### 5.1 Uniform variance comparison

Set `W_G=G(I_d-G)+(2N)^-1 I`. Its smallest eigenvalue is at least `1/(2N)`. If `q=g_{N,G}(H)`, then

\[
 \|W_G^{-1/2}HW_G^{-1/2}\|_{\rm HS}\le2q,
\]

because `(w_i+w_j)/(Nw_iw_j)<=4` entrywise. The exact variance expansion at `G+H/2` has normalized linear norm at most `q` and normalized quadratic norm at most `3q^2/4`; here `||W_G||op<=3/4`. Thus for `q<=1/4`, the midpoint and endpoint variance matrices, and their corresponding positive quadratic forms, are comparable by factors two.

For the ball calculation the same expansion at `G+tH`, `|t|<=1`, gives a normalized bound `2|t|q+3t^2q^2`. This also controls the determinant densities on sufficiently small ellipsoids. The metric lower bound first converts a sufficiently small `d_N(E,F)` into a small midpoint modulus; only then is the local form comparison used. Conversely a sufficiently small endpoint form controls the midpoint form and hence `d_N`. The resulting radius cap depends on `d` through the metric constant. No global equivalence to a fixed tangent ellipsoid is asserted.

Let `G_{N,E}` be the matrix of the real quadratic form in Hilbert–Schmidt orthonormal coordinates, and set

\[
 \rho_N(E)=\sqrt{\det G_{N,E}},\qquad d\mu_N(E)=\rho_N(E)\,dE.
\]

The determinant is positive and continuous at fixed `N`. Comparable variance matrices give density comparison within `2^(d^2/2)`. The full ambient ellipsoid `g_{N,E}(H)<=r` has Lebesgue volume `omega_(d^2) r^(d^2)/rho_N(E)`. The local metric-to-form implication and the density comparison immediately give the upper operational-ball measure bound.

### 5.2 A full legal ellipsoid at every boundary point

The lower bound does not assume a uniform legal fraction of an ellipsoid centred on a boundary. It constructs one explicitly. For a small dimension-dependent constant `a`, put

\[
 s=ar/N,\qquad E_s=(1-2s)E+sI.
\]

Then `sI<=E_s<=(1-s)I`, and a direct diagonal calculation gives

\[
 g_{N,E}(E_s-E)^2\le da^2r^2.
\]

Choose `a` sufficiently small to place `E_s` within operational distance `r/4` of `E`.

Now take the full real `d^2`-dimensional ellipsoid `g_(N,E_s)(X)<=br`. If `ell_i` are the eigenvalues of `E_s`, then `ell_i>=s` and `w_i<=ell_i+1/(2N)`. Consequently

\[
 \|E_s^{-1/2}XE_s^{-1/2}\|_{\rm HS}^2
 \le b^2\left(\frac{2r}{a}+\frac1{a^2}\right).
\]

The same estimate holds with `I-E_s` in place of `E_s`. Taking `b<=a/4` and reducing the radius cap makes both operator norms at most one half. Thus **every point** of this entire ellipsoid is a legal effect. A further fixed reduction of `b` puts it within the desired operational ball by the triangle inequality.

Its determinant-weighted measure is bounded below by a constant times `r^(d^2)`: the density at its own centre cancels against the exact ellipsoid volume. No comparison of densities across an uncontrolled boundary displacement is needed. This proves both bounds in `lem:matrixball76` uniformly at scalar effects, deterministic effects, projections of every rank, one-sided faces, and repeated spectra.

## 6. Total volume and the power of the logarithm

### 6.1 The real matrix determinant and spectral Jacobian

For `w_i=lambda_i(1-lambda_i)+(2N)^-1`, the diagonal real directions have weight `N/(2w_i)`. Each off-diagonal complex entry has two real Hilbert–Schmidt orthonormal directions, both with weight `N/(w_i+w_j)`. Therefore

\[
 \rho_N(E)=2^{-d/2}N^{d^2/2}
 \prod_iw_i^{-1/2}\prod_{i<j}(w_i+w_j)^{-1}.
\]

Differentiating `E=U diag(lambda) U*` shows that each off-diagonal complex direction contributes `(lambda_i-lambda_j)^2` to the real spectral Jacobian. The compact orbit and permutation factors depend only on `d`. At fixed `N`, the repeated-spectrum set remains null for the continuous density, so the change of variables accounts for the complete measure.

Replacing the individual cutoff `tau/2` by `tau` changes only dimension-dependent constants. Thus total measure is comparable to `N^(d^2/2) I_d(tau)`, where

\[
 I_d(\tau)=\int_{[0,1]^d}
 \prod_i(v_i+\tau)^{-1/2}
 \prod_{i<j}\frac{(\lambda_i-\lambda_j)^2}{v_i+v_j+\tau}
 \,d\lambda.
\]

The exponent `d^2/2` uses the real dimension of Hermitian matrices; it is not obtained by independently counting a spectrum and a redundant flag parameterization.

### 6.2 Upper bound from all ordered endpoint prefixes

Partition eigenvalues into a fixed interval near zero, a fixed interval near one, and a middle interval. Factors involving a middle eigenvalue are bounded above and can be integrated out. For the remaining endpoint depths order `x_1<=...<=x_l`, write `y_j=x_j+tau`, and record the endpoint by a sign `epsilon_j`.

A same-endpoint pair with earlier index `i<j` contributes at most a constant times `y_j`; an opposite-endpoint pair contributes at most a constant times `y_j^-1`. Including the individual factor gives the sector majorant

\[
 C_d\prod_jy_j^{a_j-1},\qquad
 a_j=\tfrac12+\epsilon_jS_{j-1},\qquad
 S_j=\sum_{i\le j}\epsilon_i.
\]

The decisive identity is

\[
 A_j:=\sum_{i\le j}a_i=\tfrac12S_j^2\ge0.
\]

Individual exponents may be negative, so checking only a simultaneous radial scaling would not suffice. Passing to logarithmic ratios of the ordered depths transforms the integral into a simplex integral of `exp(-sum_j A_j u_j)`, with total available logarithmic length of order `log(2+1/tau)`. Every positive `A_j` is at least one half and gives an integrable exponential direction. Every zero `A_j` gives at most one logarithmic factor. A zero requires an even prefix, so there are at most `floor(l/2)<=floor(d/2)` such factors. The finitely many endpoint sectors preserve this order.

### 6.3 Matching lower bound from nested opposite-endpoint pairs

Let `m=floor(d/2)`. Choose separated scales `tau<=t_1`, `8t_j<=t_(j+1)`, and `t_m<=1/32`. For each scale restrict one eigenvalue to `[t_j,2t_j]` and another to `[1-2t_j,1-t_j]`. If `d` is odd, keep the remaining eigenvalue in a fixed middle interval.

Within one pair the two individual factors and the opposite-endpoint factor have product comparable to `t_j^-2`. Between two separated pairs, two same-endpoint factors contribute order `t_j^2` and two opposite-endpoint factors order `t_j^-2`; their product has constant order. The integration box has volume comparable to `product_j t_j^2`. Each box therefore contributes a uniform positive amount.

Taking increasing scale tuples from powers of eight gives disjoint boxes and order `[log(2+1/tau)]^m` contributions once the logarithmic range is large enough for fixed `d`. The remaining bounded-horizon range is supplied by a fixed interior box of distinct eigenvalues. This also handles `d=1`. Proposition `prop:matrixvolume76` follows:

\[
 \mu_N(\mathfrak E_d)\asymp_d
 N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}.
\]

The disjoint boxes in this argument compute the spectral integral. Their coordinate separation is not substituted for operational packing separation.

## 7. Covering and existential rational descriptions

For any cover by radius-`delta` legal-centre balls, the uniform upper ball-measure bound yields

\[
 \mu_N(\mathfrak E_d)\le L C_d\delta^{d^2}.
\]

This establishes the converse for every legal memoryless centre of the stated binary interface. For the upper bound, take a maximal `delta`-separated set. Its radius-`delta/3` balls are disjoint and have uniformly positive measure, so its cardinality is at most a constant times `mu_N delta^-d^2`. Compactness and hybrid continuity give a finite maximal set, and maximality gives the cover. Using `delta/3` avoids any reliance on how boundaries of touching balls are measured.

Rational legal effects are dense: move each chosen centre slightly toward `I/2`, then approximate its independent real matrix entries rationally inside the resulting positive margin. Hybrid continuity controls the fixed-horizon distance. Applying this to a radius-`delta/2` cover with a `delta/2` allowance gives a rational cover of the same order.

This volume argument proves existence of optimal-order rational descriptions in each fixed dimension. Section 57 adds a deterministic rational-grid construction whose separate termination and cardinality proofs are audited in Section 10 below; that effective result is not inferred from density alone. The fixed-length payload follows from indexing a finite cover, and its converse follows because each legal reusable word supplies one memoryless centre. The law

\[
 \frac{d^2}{2}\log_2N+\lfloor d/2\rfloor\log_2\log(N+2)
 +d^2\log_2(1/\delta)+O_d(1)
\]

holds on the same stated range `N>=1`, `0<delta<=delta_d`. The power of the horizon logarithm belongs to total volume; the accuracy contribution is `d^2 log(1/delta)`.

## 8. The common qubit learning subroutine

The learner is a new uniform statistical experiment. Its inputs, branch choices, frames, block lengths, and output are functions only of the public parameters and observed records. It does not know the target pair, eigenvalues, bias, or noise. Its proof uses the upper metric theorem and concentration rather than reinterpreting the pairwise lower witnesses.

Write the effect as `((1+b)I+r u dot sigma)/2`, with `|b|+r<=1`. The future loss horizon is `N`; the total training calls are a separate quantity. The theorem assumes sufficiently small `delta` and `0<eta<=1/8`, and permits ideal trusted preparation of the specified finite qubit input states. Classical runtime, quantum memory, and hardware are not optimized.

### 8.1 Low contrast, scalar effects, and endpoint noise

A fixed coarse experiment on the six signed Pauli axes distinguishes a low-contrast branch with `r<=7/8` from a high-contrast branch with `r>=5/8` and a constant-accuracy direction, except on its assigned failure event.

In the low branch, variance-sensitive product estimates give

\[
 e=\|\widehat x-ru\|\le3(\sqrt{(1-b^2)\lambda}+\lambda),
 \qquad\lambda=L/n.
\]

Feasibility implies `1-b^2>=r(2-r)` and `V=(1-b^2-r^2)/2>=(1-b^2)/9`. Normalization of the Cartesian estimate gives `rh<=pi min(r,e)`. The angular loss is consequently at most a constant times `sqrt(Nlambda)+Nlambda`, including the scalar and deterministic limits.

Endpoint recovery requires an additional estimate. Inputs along the recovered signed axis have success parameters `p-gamma,q+gamma`, where

\[
 \gamma=\tfrac r2(1-\cos h)\le\min(r,e^2/r).
\]

For either endpoint `t=p` or `q`, one has `1-b^2<=4t(1-t)+3r`. Splitting the cases `r<=lambda` and `r>lambda` proves

\[
 \gamma\le9\sqrt{t(1-t)\lambda}+72\lambda.
\]

Thus the directional error can be absorbed into the same variance-sensitive endpoint rate, even when one endpoint is zero. Fresh observations along the random estimated axis are conditionally Bernoulli, so concentration is applied after conditioning on the earlier record. Uniform square-root-probability error is of order `sqrt(lambda)`. Sorting the two empirical probabilities preserves that error by monotonicity in the square-root angle. The aligned two-row programme then bounds spectral loss by `C sqrt(Nlambda)`. Taking `n` of order `N delta^-2 log(1/eta)` proves the required low-contrast risk.

### 8.2 Exact bias cancellation in the high-contrast experiment

For a known local frame and a transverse plane, the off-diagonal entry of the observable `2E-I` can be written `r(u dot w+i u dot e_i)`. Prepare a GHZ state with phase `phi` and a fresh fair sign `s`, use its `m` qubits, and record `s` times the product of the observed signs. Its expectation is exactly

\[
 \operatorname{Re}\left(e^{i\phi}
 [r(u\cdot w+i u\cdot e_i)]^m\right).
\]

The diagonal bias term is independent of `s` and cancels. This calculation uses the tensor product of the consuming classical-output channels and remains valid when the unused input qubits are retained between calls. It gives no environment access or coherent control of the unknown device.

Two phases in each of two transverse planes recover both complex powers from bounded observations. If the angular localization is at most `2a/m`, the true phases are unambiguous and the amplitudes lie between `.99r^m` and `r^m`. With amplitudes bounded below, complex estimation error `zeta` gives angular error at most `C zeta/m`. Both transverse coordinates are recovered by the displayed two-angle reconstruction in the proof.

### 8.3 Unknown-noise block selection and the call cap

The explicit `SelectBlock` pseudocode tries dyadic lengths up to the largest power of two not exceeding `N` and **returns immediately at the first rejection**. Each accepted stage improves the direction enough for the next length. It saves the updated direction with its accepted length. Acceptance implies a constant lower bound on `r^m`; rejection, together with the current directional localization, implies `m(1-r)` is bounded below. Returning that saved pair therefore gives

\[
 c\min\{N,(1-r)^{-1}\}\le m_*\le N,
\]

with constant amplitude and a direction accurate to order `1/m_*`. Length one is accepted when the initial cone and its sample-mean event are good. First-stage rejection returns `(1,w_0)`. Later rejection returns the preceding accepted pair, and no larger length is then tested.

Every principal argument is preceded by the algebraic guards `Re(z_i)>0` and `8|Im(z_i)|<=Re(z_i)`. On an accepted good stage, with `a=1/64`, `kappa=a/1024`, and true amplitude `rho>=1/4-kappa`,

\[
 \Re z_i\ge\rho(1-2a^2)-\kappa
 >8(2a\rho+\kappa)\ge8|\Im z_i|.
\]

Thus the guard preserves every good accepted stage and excludes zero, the branch cut, and out-of-cone phases before phase recovery. The updated error is at most `32kappa/((1/4-kappa)m)<=a/(4m)`, which implies the next-stage cone. A good rejection is necessarily an amplitude rejection and yields `r^m<(1/4+kappa)/.99<1/3`. The same elementary sine/cosine bounds verify the final guard when the amplitude is at least `1/6` and `zeta<=a/100`. Final-guard failure retains the selected axis; zero product estimates and frame ties have fixed conventions. All records therefore produce a legal effect within their public budget.

The confidence table allocates `eta/8` to the coarse six-group estimate, `eta/8` to the product branch's six fresh groups, `eta m/(32N)` to dyadic stage `m` (total at most `eta/16`), `eta/8` to fine estimation, and `eta/16` to each of the two fresh endpoint groups. The conservative sum is `9eta/16<eta`. Every noninitial concentration bound is conditional on the preceding record. With a reached-stage indicator `T_m`, the proof uses `P(T_m and G_m^c)=E[1_(T_m)P(G_m^c|F_m)]`; it assumes no independence between stage failures. The coarse error bound `1/6400` gives the explicit branch slack `3/4+1/6400<7/8` and `3/4-1/6400>5/8`.

The worst-record stage cost is bounded by

\[
 C\sum_{m\ {\rm dyadic},\,m\le N}
 m\log\frac{CN}{\eta m}\le C'N\log\frac{C'}\eta.
\]

The summable `2^-k` and `k2^-k` weights eliminate an extra `log log N`; this bound includes confidence failures. Each of the four settings uses the prescribed integer block count `ceil(4zeta^-2 log(8/epsilon))`. The explicit whole-path call budget includes these ceilings and all possible later dyadic stages, even after an early return. In particular the budget is not restricted to successful records.

At the final length, choose complex accuracy proportional to `delta sqrt(m_*/N)`. It costs order `N delta^-2 log(1/eta)` calls and yields angular error of order `delta/sqrt(Nm_*)`. High-contrast feasibility gives `r(1-r)<=V<=1-r`, so `m_*(V+1/N)` has a positive lower bound. The angular metric loss is therefore at most its allocated fraction of `delta`. The induced endpoint displacement is of order `delta^2/N`. Fresh signed-axis observations recover both endpoint probabilities in square-root distance at rate `delta/sqrt(N)`, including singular endpoints. The aligned programme and sorting argument complete the risk proof. Every GHZ block is at most `N`, while the training-call total can be much larger than the future horizon.

### 8.4 Matching lower bound and the rational output

For the converse take scalar effects `I/2` and `(1/2+Delta)I`, with `Delta=256delta/sqrt(N)` and a sufficiently small absolute accuracy cap. The preserved Bernoulli lemma separates their future-horizon distances by strictly more than `2delta`. Any adaptive training experiment on this scalar subfamily is a common channel of its independent Bernoulli bits; references and input choices supply no additional parameter-dependent information. Its relative entropy is at most `3MDelta^2` for `M` worst-record calls.

A uniformly accurate learner would distinguish the two disjoint success balls with each error at most `eta`. The elementary fidelity/relative-entropy testing bound therefore gives

\[
 M\ge cN\delta^{-2}\log(1/\eta),\qquad0<\eta\le1/8.
\]

The proof includes the short testing inequality, so this lower bound does not rely on an unproved equivalence between estimation and pair-dependent discrimination.

For rational requested accuracy, approximate the final legal estimated bias and Bloch vector to joint error `epsilon<=delta/(100N)`, then divide both by `1+2epsilon`. The result is rational and legal, with one-use distance at most `3epsilon` from the estimate. The hybrid bound and the preserved qubit code at a constant rescaling of accuracy fit within the reserved loss allowance. This produces one charged rational word without further device calls. The rounding starts from the learned estimate and does not require the unknown exact matrix.

## 9. Common learning in arbitrary input dimension

### 9.1 Endpoint-sensitive calibration

Section 56 does not learn arbitrary matrix entries in one fixed uncalibrated basis and assume that the resulting compression losses control the full measurement. Such a restriction could introduce variance above the finite-horizon cutoff. The calibration instead returns a legal estimate `A` with simultaneous comparisons of both support endpoints and the additional operator-norm accuracy

\[
 \tfrac12(A+\tau I)\preceq E+\tau I\preceq2(A+\tau I),
 \qquad
 \tfrac12(I-A+\tau I)\preceq I-E+\tau I\preceq2(I-A+\tau I),
 \qquad\|E-A\|_{\rm op}\le\sqrt\tau,
 \quad\tau=N^{-1}.
\]

At scales `t_j=2^-j`, the procedure uses `h_d=2d^2-d` product input settings in an eigenbasis of the preceding legal estimate, `K_d=(320d)^2`, and per-setting sample count `ceil(K_d t_j^-1 L_j)`. The diagonal states and both real/imaginary signed superpositions determine the Hermitian entries. The imaginary half-difference uses the frequency on `(e_i-i e_j)/sqrt(2)` minus that on `(e_i+i e_j)/sqrt(2)`; this sign is fixed in the source.

Conditional Bernstein bounds give simultaneously

\[
 |(B_j-E)_{ij}|\le\sqrt{2(E_{ii}+E_{jj})q}+2q,
 \qquad
 |(B_j-E)_{ij}|\le\sqrt{2(2-E_{ii}-E_{jj})q}+2q,
 \quad q=L_j/n_j.
\]

The complex-coordinate factor includes both quadratures. In the preceding estimate's eigenbasis, division by `sqrt((a_i+t_j)(a_j+t_j))` gives at most `5/sqrt(K_d)`; the same bound holds for complementary eigenvalues. The Hilbert–Schmidt-to-operator estimate is at most `1/64` because there are `d^2` entries. The preceding dyadic invariant gives `A+tI <= 4(E+tI)` and its complement, producing the simultaneous relative error bounds with `alpha=1/16`.

On this event the raw estimate already has spectrum in `[-alpha t,1+alpha t]`, so its prescribed clipping does nothing. The update `(B+alpha tI)/(1+2alpha t)` is legal on every record and preserves the endpoint invariant, with actual factors `7/8` and `9/8` before weakening to two. The unweighted error satisfies `||B-E||_op <= sqrt(t)/80`; rescaling adds at most `alpha t`. This proves the required `sqrt(t)` operator bound. For `N=1`, returning `I/2` without calibration samples meets the stated conclusions.

Eigenbasis selection is total and effective on the recorded data: calibration matrices are algebraic in the fixed public input basis; ordered spectral projections and fixed-order Gram–Schmidt resolve multiplicities and zero projections using exact algebraic arithmetic. No exact spectral information about the unknown `E` is supplied. Clipping and subsequent fixed sample counts define the procedure even outside concentration events.

With `H=2^ceil(log2 N)` and allowances `epsilon_j=epsilon 2^j/(4H)`, their sum is below `epsilon/2`. Conditional union bounds apply at every reached stage. The weighted sum `sum_j 2^j L_j` is `O(N log(d/epsilon))`; ceilings contribute at most the same order. Multiplying by `h_d K_d` gives `O(d^4 N log(d/epsilon))` calls on every record. Here `H` indexes calibration precision, while every calibration experiment uses a single input, so it does not violate the entangled-block cap.

### 9.2 Harmonic means and compression variance

Let `W_G=G(I-G)+tau I/2`. The proof compares the two regularized endpoints through

\[
 R_G=((G+\tau I)^{-1}+(I-G+\tau I)^{-1})^{-1}
 =\frac{G(I-G)+(\tau+\tau^2)I}{1+2\tau}.
\]

For `0<tau<=1`, this lies between `(G(I-G)+tau I)/3` and `G(I-G)+tau I`. Invert the endpoint orders, add, and invert again. This compares `R_E,R_A` within factors two, hence the regularized variances within factors twelve:

\[
 \tfrac1{12}W_A\preceq W_E\preceq12W_A.
\]

For a projection `P` commuting with `A`, the compression `C=PEP` satisfies the exact identity

\[
 C(I-C)=PE(I-E)P+PE(I-P)EP.
\]

Because `PA(I-P)=0`, the second term equals the product of off-block errors of `E-A`, and is bounded by `tau P`. Since `PW_AP >= tau P/2`, it follows that

\[
 \tfrac1{12}PW_AP\preceq W_C\preceq14PW_AP.
\]

This is the required control of compression-induced noise; all constants are independent of support ranks and spectral multiplicities.

### 9.3 Common pair learners, assembly, and legality

For `d>=2`, use all `s=binom(d,2)` coordinate pairs in the calibrated eigenbasis. The two-dimensional channel is exactly the restriction of the original binary measurement under a known isometric embedding, including when its inputs are entangled with other inputs or a reference. Each common qubit learner receives accuracy `varepsilon=c_*delta/d` and confidence `eta/(2s)`, with fresh data. These guarantees are uniform conditional on the calibration record.

The small operational error first bounds the midpoint modulus using the dimension-two metric lower bound; only then is `lem:matrixlocal76` applied to obtain `g_(N,C)(D-C)<=A_0 varepsilon`. The compression-variance inequality gives `gamma_ij(X)<=sqrt(14)g_(N,C_ij)(X)` for the known diagonal weighted form. Taking one estimate of each diagonal entry and the corresponding estimate of every off-diagonal entry yields

\[
 g_{N,A}(B-E)^2
 \le\sum_{i<j}\gamma_{ij}(\widehat C_{ij}-C_{ij})^2
 \le14sA_0^2\varepsilon^2.
\]

Unused repeated diagonal estimates are discarded; no consistency among them is assumed. The assembled matrix need not be legal. Its projection onto the legal interval in the positive norm `g_(N,A)` is well defined, and a finite rational approximate minimizer suffices. The grid is constructed in the **fixed public input basis**, not described as rational merely in the random eigenbasis. An inward displacement followed by sufficiently fine rational coordinate rounding yields legal candidates within the required Hilbert–Schmidt mesh. The bound `g_(N,A)(X)<=N||X||_HS` and finite objective evaluations certify a selection within `varepsilon` of the minimum. All observed matrices are algebraic or computable from the finite record; no unknown-target oracle is used.

The selected rational effect obeys `g_(N,A)(F-E)<=C_0 d varepsilon`. Variance comparison gives `g_(N,E)(F-E)<=sqrt(12)C_0 d varepsilon`. Choosing the absolute multiplier in `varepsilon` sufficiently small, the endpoint-to-midpoint comparison and `d_N<=8Q_N` give loss at most `delta`. Small-error constants are chosen before this conclusion; no large-error extension is inferred.

### 9.4 Probability, training cost, and matching fixed-dimensional order

Calibration receives allowance `eta/2`, the `s` pair learners receive `eta/(2s)` each, and rational selection receives zero statistical allowance. Pair guarantees remain conditional on the observed calibration basis; no independence between its estimation error and later learned quantities is assumed. The resulting union bound is at most `eta`. Dimension one is handled by direct Bernoulli estimation.

Calibration costs `O(d^4 N log(d/eta))`; the `s` qubit learners together cost `O(d^4 N delta^-2 log(d/eta))`. These are deterministic upper bounds on every record. All entangled blocks have length at most `N`, and rational postprocessing adds no device calls. Trusted preparation, retained quantum memory, classical time, workspace, and later codeword length have their separate entries in `RESOURCE_LEDGER.md`.

The scalar pair `I_d/2` and `(1/2+256delta/sqrt(N))I_d` has the same future-loss separation and Bernoulli reduction in every dimension. Arbitrary reference-assisted adaptive training reduces to processing independent scalar outcomes with parameter-independent resources; stopped records can be padded to the public cap. The testing bound gives `M>=cN delta^-2 log(1/eta)`. Thus the training order matches for every fixed `d`. No argument establishes optimal `d^4` dimension dependence.

## 10. Effective rational matrix coding

Section 57 supplies the constructive result missing from the v76 volume-only argument. For public integers `d,N>=1` and rational `0<delta<=1`, set `K=ceil(32dN/delta)`. The legal bounded Hermitian coordinate grid is ordered lexicographically. Retain its first element and subsequently retain `G` precisely when `Q_N(G,C)^2>(delta/16)^2` for every previously retained centre. Each grid element therefore has a retained centre within that comparator threshold. This is a finite combinatorial argument and uses no triangle inequality for `Q_N`.

Legality is exact Gaussian-rational Schur elimination applied to both effects. A negative pivot rejects; a zero pivot must have a zero remaining row and column; a positive pivot passes to its Schur complement. This includes singular matrices. The regularized Sylvester coefficient matrix is invertible over the Gaussian rationals, so its solution gives rational `Q_N^2` and exact comparisons. The enumeration requires no spectral threshold or matrix-dependent advice.

For encoding, use the inward displacement with `s=2d/K`, then nearest-coordinate rounding with a specified tie rule. The operator rounding error is at most `d/K`; the inward margin ensures the rounded matrix is still legal. The total displacement from the target is at most `3d/K<=3delta/(32N)`. Choosing the first retained centre within comparator radius `delta/16` gives

\[
 d_N(E,C_j)\le2N\|E-G(E)\|_{\rm op}+8Q_N(G(E),C_j)
 \le3\delta/16+\delta/2=11\delta/16.
\]

This calculation also applies to a represented real target with certified coordinate errors at most `1/(8K)` before rounding, as quantified in the source. It does not assume unrepresented real input can be read exactly. The actual exact supplied-matrix implementation takes Gaussian-rational input and has no device-learning interface.

Distinct retained centres are separated in the genuine operational metric by more than `delta/(131072d)`. Operational balls of radius `b_d delta`, with `b_d` below both the local-ball cap and `1/(393216d)`, are disjoint. Their uniform positive measures and the total-volume theorem give

\[
 |\mathscr C_{d,N,\delta}|
 \le C_d N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]

This upper cardinality bound holds throughout the construction's rational `0<delta<=1` range because its packing radii remain inside the local cap. The matching fixed-length payload formula invokes `thm:matrixcover76` only in its small-error range `delta<=delta_d`.

Both parties reconstruct the same ordered list from public parameters. The word contains only an index of length `ceil(log2 L)` for the completed size `L`; unused words map to `I/2`. No uncharged centre coordinates or target-dependent advice are appended. If parameters are not public, their chosen header is charged separately.

The ambient enumeration has at most `(K+1)^d(2K+1)^(d(d-1))` coordinate tuples and the literal retained list occupies `O(Ld^2)` rational entries. Pairwise Sylvester solves, rational bit growth, the input description, and decoder reconstruction are additional computation costs. The result is a finite exact implementation; polynomial complexity in payload length is not claimed. `matrix_codec.py` reports a resource-limited construction as incomplete and emits no completed-codebook or payload claim. Complete small cases, kernel grids, and prefix checks are distinguished in its regression output.

## 11. A learned reusable matrix description

Corollary `cor:matrixlearnedcode77` uses the matrix learner at accuracy `delta/2`, with confidence `eta`, then passes its public-basis legal rational output to the deterministic matrix encoder at accuracy `delta/2`. On the learning event, the decoded effect has loss at most

\[
 \delta/2+11\delta/32=27\delta/32<\delta.
\]

The encoder introduces neither device calls nor a new statistical failure event. The rational requested accuracy lies in the intersection of the learner's absolute small-error range and the entropy theorem's dimension-dependent small-error range. Constant rescaling preserves both `Theta_d(N delta^-2 log(1/eta))` training order and the optimal fixed-length payload. This is a composition of the **unknown-device** statistical interface with the **supplied-estimate** computational interface. It does not acquire an exact target description as a free input or identify the training record, classical workspace, or reconstructed dictionary with the payload.

## 12. Retained qubit proof and exact implementation

Sections 51–52 retain the all-pair qubit comparison, the exact scalar-overlap angular construction, both lower angular regimes, the projective-corner packing, and the matching rational lattice count. The new matrix converse depends explicitly on the preserved nonadaptive qubit theorem. The earlier unbiased weighted-volume and boundary-contact results retain their own identifiable-image regularity assumptions and error caps; the matrix-body volume theorem does not overwrite those family results.

The qubit angular coefficient remains

\[
 K_N(p,q)=(p-q)\sqrt{\frac N{p(1-p)+q(1-q)+N^{-1}}}.
\]

Both endpoint probabilities matter. At `q=0` with fixed `0<p<1`, this has square-root horizon order. At `p=q` the direction vanishes and the exact residual problem is Bernoulli. At the projective endpoint the inherited exact result remains separately identified. The scalar-overlap gauge is pairwise and acts only on inaccessible environments; it is not a global seizer. Publicly stopped testers are padded. The aligned spectral rows provide an upper programme bound, not a general exact product formula.

The four-dimensional qubit cover continues to discretize both corner depths and charge both eigenvalues together with direction. Its cutoff lattice produces `log(N+2)` with no additional accuracy logarithm. A scalar spectral level carries one codeword, while every overlapping signed stereographic chart word is counted. Exact radical comparisons retain sign checks before squaring. Type validation remains outside cached layout lookup, including populated-cache Boolean/integer collisions.

Every valid in-range decoded word is legal. Canonical replay for a supplied target checks its deterministic selected index; it does not identify each target injectively, reject every different target in the same cell, or numerically evaluate the exact adaptive distance. Approximation follows from the proved encoder and its construction budget. The implementation uses `O(B^2)` exact arithmetic operations and `O(B)` retained spectral values/row starts, with `B=ceil(sqrt(64N/delta^2))`; this is not a polynomial bound in all numerical input lengths or a claim of optimal workspace.

## 13. The r50 D01–D36 technical checks

This table records the inherited v76 obligations and their v77 proof interfaces. It supplements the detailed calculations above; a row is not a claim that a finite regression proves the corresponding continuum theorem. D36 concerns external editorial judgment and is not converted into a theorem certificate.

| Comment | Checked point and source interface |
| --- | --- |
| D01 | `d_N` uses unhalved trace norm; classical total variation is half its classical value. Section 53 and this audit retain the exact one-use normalization. |
| D02 | The nonadaptive class allows input-block entanglement and retained references but no feedback. The adaptive comparison is a constant-factor inequality, not equality of optimal experiments. |
| D03 | Outcome copies and factor environments introduced in a purification remain inaccessible to the tester. They are analytical dilations of the same observed binary channel. |
| D04 | Multiplication by the square-root factors proves `T_y+T_y^*=0` from the differentiated effect identity. This realizes the horizontal tangent by genuine nearby factors. |
| D05 | The Sylvester remainder is inserted at the differential level in a fixed tester. It is not a convex decomposition of a finite pair of devices. |
| D06 | A publicly stopped tester is padded with fixed dummy inputs whose outputs and auxiliary environments are discarded. The original observed output is unchanged. |
| D07 | The interior approximation is taken at fixed `N`; hybrid continuity and the regularized form justify this limit. No interchange uniform in `N` is asserted. |
| D08 | Loewner order passes to left-plus-right multiplication through `2 tr((V_G-aV_M)X^2)>=0` on Hermitian `X`. Positivity of left multiplication alone is not used. |
| D09 | The lower-bound factor `d` comes from the largest of `d^2` weighted entries. It is not an optimal dimensional constant. |
| D10 | Two-dimensional compression is an isometric input restriction, exact also on entangled/reference inputs. Section 56 adds learned calibration before using many such restrictions together. |
| D11 | A zero compressed gap has zero angular term and needs no eigendirection. Scalar limits remain part of the closed-body statements. |
| D12 | The ordered spectral intersection vector depends on the supplied pair and on its index. The proof does not produce one simultaneous witnessing basis. |
| D13 | Small operational loss is converted into a small midpoint modulus before applying local form comparison. This order is used again in Section 56. |
| D14 | Boundary balls use an inward displacement of order `r/N`; a full legal ellipsoid is then placed around the displaced point. No fixed legal fraction of a boundary-centred ellipsoid is assumed. |
| D15 | The covering converse permits every legal centre in the effect body, including singular and repeated-spectrum centres. |
| D16 | Determinants use the real Hilbert–Schmidt orthonormal Hermitian basis: a diagonal direction and two real directions for each complex off-diagonal entry. |
| D17 | The complex-Hermitian spectral Jacobian has a squared Vandermonde; orbit and permutation factors depend only on fixed `d`. Multiplicity strata are handled metrically before integration. |
| D18 | A zero signed prefix has even index; the number of zero prefixes, not the number of boundary eigenvalues, determines the logarithmic power. |
| D19 | Separated opposite-endpoint pairs retain the explicit same-endpoint/opposite-endpoint cross-factor cancellation that yields the nested lower boxes. |
| D20 | Density alone proves rational existence. Section 57 separately provides a fixed rational enumeration, exact selection, termination, payload accounting, and stated computational bounds. |
| D21 | The coarse vector error `1/6400` gives `3/4+1/6400<7/8` and `3/4-1/6400>5/8`, with normalization inside the initial angular cone. |
| D22 | Sorting is nonexpansive in the `arcsin sqrt(t)` coordinate and preserves the uniform Hellinger endpoint estimates, including zero and one. |
| D23 | Final endpoint samples are fresh after the axis is fixed; their conditional parameters are exactly `p-gamma` and `q+gamma`. |
| D24 | Each GHZ block has its own independent fair sign conditional on the preceding record. The unknown diagonal bias cancels exactly in the signed parity mean. |
| D25 | Both transverse planes and both quadratures are used, recovering the two local angular coordinates. |
| D26 | The maintained cone and total algebraic phase guard keep the principal argument unambiguous. No global unwrapping theorem is imported. |
| D27 | The first amplitude or phase rejection returns the preceding accepted-and-updated pair immediately. There is no later scale or retry. All first-stage and final-phase fallbacks are specified. |
| D28 | Reached-stage conditional failure allowances sum geometrically to at most `eta/16`; no independence between their failure events is required. The full qubit ledger also charges the product branch's fresh six groups. |
| D29 | The `2^-k` and `k2^-k` weighted logarithmic sums give `O(N log(1/eta))` selector cost, including bad records and ceilings. Matrix calibration uses the same summable-budget principle. |
| D30 | The exact cancellation `m_* zeta_*^-2=c_*^-2 N delta^-2` controls the final refinement at every returned length. |
| D31 | Scalar effects reduce arbitrary adaptive reference-assisted training to independent Bernoulli outcomes and common processing. The same converse applies in every input dimension. |
| D32 | Learned outputs are made legal and rational before exact coding; reserved radius slack pays for postprocessing with no additional device calls. The matrix composition has total loss at most `27delta/32`. |
| D33 | The common learner is a written algorithm, and its finite checks are not a full stochastic implementation or continuum risk certificate. The separate supplied-matrix codec is implemented, with execution scope explicitly reported. |
| D34 | The structural companion is inherited and retains its fresh nondisturbing classical-probe interface. It is not a result about repeated calls to the consuming quantum measurement. |
| D35 | The v76 object supplies the v77 baseline of 658 active complete-edition labels and 296 native source files. The older 557/266 counts compare v76 to v75, and must not be reused as the v77 baseline. Preservation is distinct from fresh independent review of every inherited proof. |
| D36 | The r50 report separates its significance judgment from proof correctness. V77 adds the arbitrary-dimensional common learner and effective matrix code; independent editorial and priority assessments remain separate from this internal audit. |

## 14. Literature, preservation, analytic obligations, and evidence

`LITERATURE_AUDIT.md` and the journal-facing comparison state the priority boundary against measurement tomography, channel learning, channel-extension geometry, adaptive discrimination, and multiscale estimation. The inherited horizontal gauges, inverse-Sylvester forms, concentration estimates, and testing reductions retain their antecedents. The theorem package audited here is the specific finite-horizon matrix comparison, its closed-body entropy, calibrated common learning at the future-loss scale, and deterministic optimal-order rational descriptions. No theorem-level comparison or bounded search is represented as independent human priority clearance.

The focused article presents the current theorem chain and its required dependencies. The complete edition and preserved native files retain the historical proofs, with the structural and quantitative interfaces separately identified. `FROZEN_R50_PIPELINE_AUDIT.md` records **658 active complete-edition labels and 296 native source files** for the completed v76 baseline. Those are predecessor counts, not asserted new v77 totals. `PRESERVATION_MANIFEST.json`, `PROOF_TEXT_PRESERVATION.json`, generated theorem locations, and the publication receipt provide the current count and exact changed/retained-source accounting. No current label or page total is estimated here. Full-proof preservation establishes source continuity; it is not a new independent audit of every theorem inherited across all revisions.

The separate analytic graph remains `A1 independent`, `A2 -> A3 -> A4 -> C2 -> D1`, and `B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`. Its raw local-limit, stopped-path, global-kernel, conditioning, process-limit, Mosco/Nisio, filtering/LAN, changing-filtration, and posterior obligations retain their own source hypotheses and status fields. The matrix theorems and bounded tester-padding argument do not update aggregate analytic flags. The historical audit records the source-specific dependencies rather than inferring their closure from finite-dimensional work.

The relevant finite evidence has deliberately limited scope:

| Evidence | Recorded computation | What it does not establish |
| --- | --- | --- |
| `check_common_learning.py` | 135,994 rational/Gaussian-rational checks and 96 negative controls, including GHZ expansion, bias cancellation, variance identities, budgets, phase guards, and finite first-rejection transcripts | A complete stochastic learner execution, a uniform probability-risk certificate, or the continuum minimax theorem |
| `matrix_codec_check.py` | 1,038 exact assertions; complete one-dimensional theorem dictionaries, complete small coarse matrix kernel grids, noncommuting matrix kernels, legality/rounding, replay, invalid-input controls, and an explicitly incomplete two-dimensional theorem-grid prefix | A fully enumerated theorem dictionary in dimension at least two, a large-dimension efficiency result, or the continuum entropy theorem |
| Retained matrix/codec regressions | Their emitted exact-algebra, supplied-pair, canonical-decoding, and defensive-parser cases | Optimization of the adaptive supremum, all possible learner records, or a proof of every continuum inequality |
| Ordinary/optimized agreement and source reconstruction | Agreement for the executed scripts and the exact recorded source object | Human authorship, independent mathematical priority, or journal acceptance |

The counts above identify the finite regression suites described in this revision; the generated outputs and final build receipt determine what was actually executed on the submitted source object. Neither algebraic examples nor codebook prefixes substitute for the written proofs. Internal agent cross-review is a separate author-side activity, and is not relabeled as human external review.

Source hashes, theorem locations, page checks, package inventories, and the receipt under `evidence/` establish reproducibility only for their recorded source object. Final-head read-only reconstruction must identify the actual submitted commit; an earlier successful run is not evidence for an unchecked successor. The recorded v76 exact-head reconstruction is predecessor evidence. Current page counts and completion claims belong to the regenerated v77 receipt. Human author signing, independent priority clearance, and editorial judgment remain separate from this audit and its build evidence.
