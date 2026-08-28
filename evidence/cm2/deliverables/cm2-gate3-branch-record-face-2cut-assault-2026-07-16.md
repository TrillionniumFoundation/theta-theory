# CM2 Gate 3: branch-record MT_DQ and FACE_2CUT direct assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: v52, the corrected depth-one DQ, the ninth-pass telescope,
product-depth kernel, controlled `s=0` recovery bridge, and the finite-`s`
common-mesh recovery manifest  
Strict verdict: **the limiting face--product type algebra and an auxiliary
depth/recovery clock layer uniform on `|s|<=1/400` are certified; dynamic branch-record
`MT_DQ`, physical `FACE_2CUT`, `FACE_TIME`, and Gate 3 remain
`NOT_CERTIFIED`**

## 1. Result

This assault closes the largest Gate-3 layer implied by the ninth-pass
evidence without promoting the formal telescope to analytic convergence.

Certified here:

1. the corrected limiting 64-row graph current is completed to the exact
   face--product centered cluster required by v52, using its actual
   marginals and with explicit typed norm bounds;
2. the product stopped-depth law gives an exact positive auxiliary depth
   tail after the full `2^K` parent-normalization charge;
3. the finite-parameter affine recovery clock turns that auxiliary tail into
   an exponentially summable depth-plus-recovery tail uniformly on
   `|s|<=1/400`;
4. the recovery moment and any proper-family coupling rate give a summable
   two-time **clock array** by an exact Markov/recovered-core split;
5. three exact countermodels isolate why none of those statements supplies
   the missing branch-record atlas, physical `FACE_2CUT`, or product-time
   current bound.

No claim is made that the auxiliary stopped depth `K` is the genuine
physical face-word depth `ell`.  The moving dyadic endpoints defined by
`u_{e,s}` are not registered in the Gate-3 common DQ atlas.  No claim is made
that the clock array already bounds the signed physical face pairing; the
certified face current remains only the limiting `s=0` cluster of Section 2.

## 2. Limiting face--product centered cluster

Let `J_V` be the corrected limiting graph current.  The frozen certificates
give the following unnormalized bounds; every displayed current norm below
carries the same final factor `Z_N^-1`:

```text
||J_V||_TV <= 16128/5,
J_V(1,1)=0.
```

With the actual marginals

```text
m_V^-=(pr_-)_*J_V,
m_V^+=(pr_+)_*J_V,
```

the v52 product correction specializes to

```text
P_V=-m_V^- tensor mu_0-mu_0 tensor m_V^+,
D_cur J_V=J_V+P_V.
```

Both marginals of `D_cur J_V` vanish exactly.  The product block pairs to
zero with two individually centered endpoint tests, so the cluster pairing
equals the graph pairing on those tests.  Contractivity of marginal
pushforward gives the numeric typed bounds

```text
||P_V||_P_R <= 32256/5,
||J_V||_TV+||P_V||_P_R <= 48384/5.
```

This closes the limiting `s=0` face--product type algebra.  It does not
construct the finite-`s` quotient cluster or prove convergence of its
marginals on an iterated common atlas.

## 3. Exact auxiliary depth and recovery tails

The query-independent product kernel has

```text
w_K=(3/4)4^-K,
2^K atoms at level K,
one atom joint mass=(3/4)8^-K m_e,
parent-normalization charge=2^K.
```

After summing all atoms and paying the complete parent charge, the positive
charged level mass is exactly

```text
a_K=2^K w_K=(3/4)2^-K.
```

Consequently

```text
sum_K a_K=3/2,
sum_(K>L) a_K=(3/4)2^-L.
```

Thus the bare auxiliary return exponent `log(4)` beats the parent-charge
growth exponent `log(2)` by the strict margin `log(2)`.

The finite-`s` common-mesh recovery theorem gives constants `A0,A1`, uniform
over the compact configuration window and both orientations, with

```text
R_fw(s,K,j)+R_rev(s,K,j) <= 2A0+2A1 K,
|s|<=1/400.
```

For every

```text
0<gamma<log(2)/(2A1),
```

the charged level is uniformly at most

```text
(3/4) exp(2 gamma A0)
      (exp(2 gamma A1)/2)^K.
```

The ratio is strictly below one.  This gives an explicit geometric tail and
replays the ninth-pass conclusion

```text
sup_(|s|<=1/400)
E_s[2^K exp(gamma(R_fw+R_rev))] < infinity.
```

This is a controlled auxiliary depth/recovery tail uniform on the full
parameter window.  Its atoms are cut, for each fixed `s`, by the moving
coordinates `u_{e,s}`.  Those moving dyadic endpoints are explicitly not in
the Gate-3 component-indexed common DQ atlas.  Physical `FACE_2CUT` still
requires an immutable record map from genuine face-word depth to the
propagated physical `q` law, with all actual/split constituents and
multiplicities included before cancellation.

## 4. Two-time clock arithmetic

Put

```text
M_gamma=sup_(|s|<=1/400)
        E_s[2^K exp(gamma(R_fw+R_rev))].
```

For either oriented clock and `N=max(m,n)`, Markov's inequality gives

```text
sup_s E_s[2^K 1_{R_o>delta N}]
 <= M_gamma exp(-gamma delta N).
```

If a properly matched recovered current couples at one rate `c_mix>0`
uniform on `|s|<=1/400`, the core `R_o<=delta N` contributes the clock factor

```text
exp(-c_mix(1-delta)N).
```

Balancing the two exponents with

```text
delta=c_mix/(gamma+c_mix)
```

gives

```text
kappa=gamma c_mix/(gamma+c_mix)>0,
C exp(-kappa max(m,n)).
```

The array is absolutely summable because, for `x=exp(-kappa)<1`,

```text
sum_(m,n>=0) x^max(m,n)=(1+x)/(1-x)^2.
```

This closes the **uniform finite-`s` clock algebra only**.  To instantiate v52
`FACE_TIME_REC`, the same physical occurrence must still be represented
recordwise as a signed difference of proper families; its restricted source
norm and scalar current must be dominated by the propagated `q` law; and the
physical bilinear test must lift to the relevant standard-family/flux-face
norms.  None of those three interfaces is supplied by the new finite-`s`
recovery manifest.  In particular, its moving dyadic endpoint mesh is not a
component-indexed Gate-3 DQ atlas, and it does not construct the finite-`s`
face--product quotient cluster.

## 5. Why the fixed-time telescope cannot be promoted

An exact Banach-space countermodel shows that the missing branch-source
invariance is substantive.

Let

```text
X=l2,
Y={y: sum k^2 |y_k|^2<infinity},
x=(1/k),
P0 z=z_1 x,
A_k z=k z_k e_1,
s_k=1/k,
P_(s_k)=P0+s_k A_k.
```

Then `P_(s_k)->P0` strongly on `X` and the family is uniformly bounded.
For every fixed `y in Y`,

```text
||A_k y||=|k y_k| ->0,
```

so the depth-one DQ converges on every fixed strong source.  The formal
depth-two telescope is exact.  However

```text
P0 e_1=x notin Y,
A_k P0 e_1=e_1,
P_(s_k) A_k e_1=0.
```

Hence

```text
(P_(s_k)^2-P0^2)e_1/s_k=e_1
```

for every `k>=2`.  The depth-two quotient does not converge to the formal
zero derivative.  The failed operation is precisely applying the
depth-one derivative to an iterated source outside its certified source
space.  Therefore the ninth-pass word cancellation cannot replace
branch-record strong-space invariance or an operator-norm DQ theorem.

## 6. Why one common moving atlas and boundary tightness are mandatory

Take `J_s=delta_s`, `J_0=delta_0` on `[-1,1]`.  Then

```text
||J_s-J_0||_BL* <= s ->0.
```

For the singular boundary `S={0}` and branchwise test
`Phi=1_(0,1]`, with `Phi(0)=0`, the test is bounded--Lipschitz on every
fixed complement of `[S]_rho`, but

```text
J_s(Phi)=1,
J_0(Phi)=0.
```

The missing clause is exactly boundary tightness:

```text
sup_(0<s<rho) |J_s|([S]_rho)=1.
```

Thus weak current convergence and branchwise convergence away from moving
cuts are insufficient.  The required object is the v52
component-indexed common atlas `A_(L,m,n)` with one fixed metric, common
record maps, and uniform boundary-`Z` tightness for all iterated
singularities.  The existing 64-row atlas supplies this only at depth one.

## 7. FACE_2CUT is not a product-time majorant

The exact nonimplication array

```text
b_(m,n,ell)=1_(m=n) 2^-(ell+1)
```

has, for every fixed `(m,n)`, the exponential word-depth tail

```text
sum_(ell>L)b_(m,n,ell)=1_(m=n)2^-(L+1).
```

Thus fixed-pair `FACE_2CUT` is perfect.  But the complete face pairing is

```text
B_(m,n)=1_(m=n),
sum_(m,n)|B_(m,n)|=infinity.
```

Therefore physical `FACE_2CUT` and `FACE_TIME_CM2/REC` are logically
independent.  A fixed-`(m,n)` constant `C_(m,n)` may not be silently used as
a summable two-time envelope.

## 8. Exact remaining boundary

Dynamic branch-record `MT_DQ` still needs:

1. one component-indexed common moving atlas for every fixed `(L,m,n)`;
2. fixed-time strong-space invariance and convergence of `Q_s^m` sources;
3. a common BL modulus for moving branch tests off the singular boundary;
4. boundary-`Z` tightness on every iterated singularity/atlas boundary;
5. regular, face, product-current, and response convergence on that same
   atlas.

Physical `FACE_2CUT` still needs:

1. a record-preserving identification of physical word depth;
2. positive coarea domination by the propagated physical `q` law;
3. a finite-`s`, no-`|s|^-1` per-depth bound;
4. actual/split constituent and component multiplicity accounting;
5. the positive deep remainder beyond `L(s)`.

Product-time face summability still needs physical current/proper-family
matching, restrictionwise `q` domination, the bilinear physical test lift,
and finite-`s` uniform signed coupling after that physical-current matching.

## 9. Latest technology audit

An arXiv search on 2026-07-16 for dispersing billiards, moving scatterers,
linear response, standard families, and characteristic-function
restrictions found no theorem newer than the ninth-pass audit that supplies
these interfaces.

Stenlund--Young--Zhang, `arXiv:1210.0011v4`, Lemmas 12 and 16 now supply the
uniform one-time recovery used on the compact configuration class.  They do
not register the moving dyadic endpoints in a Gate-3 DQ atlas or construct
the physical face-current norm lifts.

Demers--Liverani, `arXiv:2606.10155v1`, Problem 8.7 states that general
loss of memory after the relevant characteristic-function restrictions is
still open because selected densities can concentrate on atypical
trajectories.  Canestrari, `arXiv:2604.19671v2`, Lemma 6.14 supplies the
closed-map Growth Lemma used by the earlier `s=0` recovery bridge, but not a
finite-`s` moving-face DQ atlas, hereditary repeated-cut recovery, or the
three-space physical norm lift.

## 10. Reproduction

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate3_branch_record_face_2cut_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python \
  deliverables/cm2_gate3_branch_record_face_2cut_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate3_branch_record_face_2cut_frontier_verifier.py
```

The first two commands exit zero.  The live default exits `2` by design
because dynamic branch-record `MT_DQ`, physical `FACE_2CUT/FACE_TIME`, and
Gate 3 remain open.
