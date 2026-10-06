# Written-proof audit — Revision 76

This is an author-side adversarial audit of the written theorem chain. It records the mathematical mechanisms, endpoint checks, quantifiers, and interfaces examined for the r49 revision. It is distinct from an independent human referee opinion, a proof-assistant certificate, an exhaustive priority determination, and a source-reconstruction record. The controlling reports are the v75/r49 external report at `4de14a3fe5c271c77de64e410e1bd67fa2e7dce8` and pipeline audit at `8ee073109d5911c6526ff81314bede13bafe9f6c`; both review final v75 head `16b78c8edef566300ea21300908854ad83455879`.

The complete r49 response is in `RESPONSE_TO_REFEREE.md`, with separate matrices for all twenty required revisions and thirty-six detailed comments. The predecessor audit is preserved under `predecessor-v75-audit/`.

## 1. The new statements and their different scopes

| Statement | Mathematical object | Quantifiers and resource |
|---|---|---|
| `thm:matrixmetric76` | The complete ordered binary effect body on `C^d` | Every finite `d`, every integer `N>=1`, every pair, all support ranks and multiplicities; comparison constants depend on `d`. |
| `lem:matrixball76` | Actual operational balls in that body | Uniform two-sided measure bounds at all centres for sufficiently small radii, with dimension-dependent constants. |
| `thm:matrixcover76` | The same complete body | Fixed `d`, all `N>=1`, `0<delta<=delta_d`; arbitrary legal memoryless centres in the converse; rational centres attain the same order existentially. |
| `thm:commonlearn76` | The complete ordered binary **qubit** body | One common learner, uniform failure at most `eta`, sufficiently small `delta`, `0<eta<=1/8`; training calls of order `N delta^-2 log(1/eta)`, where `N` is the future loss horizon. |
| `thm:biasedcodec75` | Rational Cartesian qubit effects | Implemented exact encoder and legal decoder; one charged index; target approximation from the written construction and canonical replay. |

The device has two ordered outcomes, consumes its input, and supplies no residual quantum output. The full-dimensional results concern arbitrary Hermitian effects, not a fixed-block subclass, a commuting family, or only a regular spectral stratum. The learner and implemented optimal codec have their separately stated qubit scope. In the inherited codec, `dimension` equal to two or three counts Bloch coordinates, not the Hilbert input dimension `d` of the matrix theorem.

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

This proves existence of optimal-order rational descriptions in each fixed dimension. It does not implement an optimal all-dimensional encoder, bound its classical runtime, or infer an efficient physical simulator. The fixed-length payload follows from indexing the finite cover, and its converse follows because each legal reusable word supplies one memoryless centre. The law

\[
 \frac{d^2}{2}\log_2N+\lfloor d/2\rfloor\log_2\log(N+2)
 +d^2\log_2(1/\delta)+O_d(1)
\]

holds on the same stated range `N>=1`, `0<delta<=delta_d`. The power of the horizon logarithm belongs to total volume; the accuracy contribution is `d^2 log(1/delta)`.

## 8. A separate common learner on the qubit body

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

Try dyadic lengths up to the largest power of two below `N`. Each accepted stage improves the direction enough for the next length. Acceptance implies a constant lower bound on `r^m`; rejection, together with the current directional localization, implies `m(1-r)` is bounded below. Returning the previous accepted length therefore gives

\[
 c\min\{N,(1-r)^{-1}\}\le m_*\le N,
\]

with constant amplitude and a direction accurate to order `1/m_*`. Length one is accepted on the coarse good event, so the returned object is defined there. Deterministic legal fallbacks define it on all exceptional records.

The stage failure allowance is proportional to `eta m/N`. Conditional concentration and a union bound control the complete data-dependent decision tree. The worst-record stage cost is bounded by

\[
 C\sum_{m\ {\rm dyadic},\,m\le N}
 m\log\frac{CN}{\eta m}\le C'N\log\frac{C'}\eta.
\]

The summable dyadic weights eliminate an extra `log log N`; this is a bound even on records where the confidence events fail.

At the final length, choose complex accuracy proportional to `delta sqrt(m_*/N)`. It costs order `N delta^-2 log(1/eta)` calls and yields angular error of order `delta/sqrt(Nm_*)`. High-contrast feasibility gives `r(1-r)<=V<=1-r`, so `m_*(V+1/N)` has a positive lower bound. The angular metric loss is therefore at most its allocated fraction of `delta`. The induced endpoint displacement is of order `delta^2/N`. Fresh signed-axis observations recover both endpoint probabilities in square-root distance at rate `delta/sqrt(N)`, including singular endpoints. The aligned programme and sorting argument complete the risk proof. Every GHZ block is at most `N`, while the training-call total can be much larger than the future horizon.

### 8.4 Matching lower bound and the rational output

For the converse take scalar effects `I/2` and `(1/2+Delta)I`, with `Delta=256delta/sqrt(N)` and a sufficiently small absolute accuracy cap. The preserved Bernoulli lemma separates their future-horizon distances by strictly more than `2delta`. Any adaptive training experiment on this scalar subfamily is a common channel of its independent Bernoulli bits; references and input choices supply no additional parameter-dependent information. Its relative entropy is at most `3MDelta^2` for `M` worst-record calls.

A uniformly accurate learner would distinguish the two disjoint success balls with each error at most `eta`. The elementary fidelity/relative-entropy testing bound therefore gives

\[
 M\ge cN\delta^{-2}\log(1/\eta),\qquad0<\eta\le1/8.
\]

The proof includes the short testing inequality, so this lower bound does not rely on an unproved equivalence between estimation and pair-dependent discrimination.

For rational requested accuracy, approximate the final legal estimated bias and Bloch vector to joint error `epsilon<=delta/(100N)`, then divide both by `1+2epsilon`. The result is rational and legal, with one-use distance at most `3epsilon` from the estimate. The hybrid bound and the preserved qubit code at a constant rescaling of accuracy fit within the reserved loss allowance. This produces one charged rational word without further device calls. The rounding starts from the learned estimate and does not require the unknown exact matrix.

## 9. Retained qubit proof and exact implementation

Sections 51–52 retain the all-pair qubit comparison, the exact scalar-overlap angular construction, both lower angular regimes, the projective-corner packing, and the matching rational lattice count. The new matrix converse depends explicitly on the preserved nonadaptive qubit theorem. The earlier unbiased weighted-volume and boundary-contact results retain their own identifiable-image regularity assumptions and error caps; the matrix-body volume theorem does not overwrite those family results.

The qubit angular coefficient remains

\[
 K_N(p,q)=(p-q)\sqrt{\frac N{p(1-p)+q(1-q)+N^{-1}}}.
\]

Both endpoint probabilities matter. At `q=0` with fixed `0<p<1`, this has square-root horizon order. At `p=q` the direction vanishes and the exact residual problem is Bernoulli. At the projective endpoint the inherited exact result remains separately identified. The scalar-overlap gauge is pairwise and acts only on inaccessible environments; it is not a global seizer. Publicly stopped testers are padded. The aligned spectral rows provide an upper programme bound, not a general exact product formula.

The four-dimensional qubit cover continues to discretize both corner depths and charge both eigenvalues together with direction. Its cutoff lattice produces `log(N+2)` with no additional accuracy logarithm. A scalar spectral level carries one codeword, while every overlapping signed stereographic chart word is counted. Exact radical comparisons retain sign checks before squaring. Type validation remains outside cached layout lookup, including populated-cache Boolean/integer collisions.

Every valid in-range decoded word is legal. Canonical replay for a supplied target checks its deterministic selected index; it does not identify each target injectively, reject every different target in the same cell, or numerically evaluate the exact adaptive distance. Approximation follows from the proved encoder and its construction budget. The implementation uses `O(B^2)` exact arithmetic operations and `O(B)` retained spectral values/row starts, with `B=ceil(sqrt(64N/delta^2))`; this is not a polynomial bound in all numerical input lengths or a claim of optimal workspace.

## 10. Literature, preservation, analytic obligations, and evidence

The active literature comparison adds the two direct references requested in r49. Krawiec–Pawela–Puchała treats rank-one POVMs and includes a nine-outcome qutrit adaptive perfect-discrimination example. Datta–Biswas–Saha–Augusiak treats single-use nonprojective entanglement-assisted discrimination, including two three-outcome qubit POVMs. Their outcome sets and objectives are distinguished from the present binary all-pair comparison, cover, and common learner. The horizontal gauge, channel-extension, integration, phase-estimation, classical concentration, and testing ingredients have established antecedents. The submitted increments are the concrete regularized matrix comparison with matching compressions, the boundary-uniform ball theorem and nested endpoint integral, and the complete biased-qubit future-horizon learner. `LITERATURE_AUDIT.md` records the theorem-level comparison; no independent human priority clearance is inferred.

The focused manuscript places the new results first and retains the necessary earlier supporting proofs in its appendices. The complete edition retains the historical order and appends the new sections. Earlier directories and inherited source labels remain available; the preservation manifest and compiled theorem map supply their exact accounting. The structural companion retains its fresh, classical, nondisturbing-probe interface and is not recast as a repeated-measurement quantum theorem. Figure `fig:effectbody76` is explicitly a spectral diagram and a section of the qubit body; it carries no evidentiary weight in the estimates.

The independent analytic graph remains `A1 independent`, `A2 -> A3 -> A4 -> C2 -> D1`, and `B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`. Its raw local-limit, stopped-path, global-kernel, conditioning, process-limit, Mosco/Nisio, filtering/LAN, changing-filtration, and posterior obligations remain separate. The recorded earlier width gap and aggregate status fields are not changed by these finite-dimensional results.

Finite regression checks algebraic examples, exact arithmetic, legal decoding, indexing, and defensive parsing. Any new arithmetic or statistical controls have only the finite scope stated in their emitted results. They do not prove the adaptive supremum, the uniform continuum estimate, the spectral integral for every dimension, all learner records, priority, or editorial significance. Normal and optimized executions must agree where the build requires that gate; actual counts belong to the generated records.

Source hashes, theorem locations, page checks, package inventories, and the build receipt under `evidence/` establish reproducibility only for their recorded source object. Final-head read-only reconstruction must identify the actual submitted commit. An earlier successful run is not evidence for an unchecked successor. Human author signing and independent human priority assessment remain separate from author-side proof review and source reconstruction; neither is claimed to have been supplied here.
