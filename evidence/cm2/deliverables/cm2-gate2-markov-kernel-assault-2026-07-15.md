# CM2 Gate 2: full-mass Markov-kernel route audit

Date: 2026-07-15 (Asia/Shanghai)  
Scope: actual-SRB reverse-kernel route only; frozen v51/v52 and the shared
research log are not edited  
Verdict: **the proposed CDKM/GKM shortcut is rigorously blocked; physical
Gate 2 remains OPEN / NO-GO**

## 1. Executive result

This assault starts from the exact conditional formula

```text
p_a(x) = rho(h_a x) |h_a'(x)| / rho(x)
```

for a declared one-state full-branch quotient.  It produces two stronger
negative conclusions than the previous “not yet instantiated” audit.

1. **CDKM Theorem 4.1 cannot be applied to the exact reverse-branch kernel.**
   For any countable full-branch quotient with non-atomic stationary density,
   the finite-time law from a point is countably atomic.  Its total-variation
   distance from the stationary density is therefore maximal at every finite
   time.  Thus the CDKM base hypothesis of uniform ergodicity in total
   variation, and every Doeblin minorisation by the physical density, are
   impossible.  This remains true with the entire full-mass countable
   alphabet; it is not a truncation artefact.

2. **GKM Theorems 2.6/2.8 do not admit the needed Markovization under their
   stated hypotheses alone.**  Their map laws are independent of the current
   point (Theorem 2.8 permits a sequence of laws fixed in advance).  An exact
   projective counterexample below gives a continuous compact law field for
   which every law has a uniformly finite bi-Lipschitz moment and no
   deterministic images, yet choosing the law as a function of the current
   point preserves a two-atom stationary measure.  Hence no uniform Frostman
   estimate follows after adaptive state dependence, even with continuity.

The collision-SRB quotient itself is still not instantiated on the pilot
common vertex.  The result here does not replace that construction and does
not prove physical PPE.  It eliminates two tempting theorem shortcuts and
identifies the correct remaining functional-analytic target.

## 2. Exact obstruction to CDKM uniform ergodicity

Assume the desired physical object has been constructed.  Thus

```text
F : union_a I_a -> I,
h_a : I -> I_a,
d mu = rho(x) dx,
0 < rho_- <= rho <= rho_+ < infinity,
```

and the full physical reverse kernel is

```text
K_x = sum_a p_a(x) delta_{h_a x},
p_a(x) = rho(h_a x)|h_a'(x)|/rho(x).
```

The Perron--Frobenius identity normalizes the kernel and the density
telescopes on words.  For every finite depth `n`,

```text
K_x^n = sum_{w in A^n} p_w(x) delta_{h_w x}.
```

Since the alphabet is finite or countable, the support

```text
S_n(x) = {h_w x : w in A^n}
```

is at most countable.  The physical quotient law `mu=rho dx` is non-atomic,
so

```text
K_x^n(S_n(x)) = 1,
mu(S_n(x)) = 0.
```

Consequently, with total variation normalized as a supremum over Borel sets,

```text
||K_x^n-mu||_TV = 1                         (all x, all finite n).
```

This proves all of the following.

- `K` is not uniformly ergodic in the sense used in Cai--Duraes--Klein--Melo.
- There are no `n` and `epsilon>0` such that
  `K_x^n >= epsilon mu` for every `x`.
- A finite alphabet truncation cannot repair the issue; it remains atomic.
- Keeping the full countable tail cannot repair it; it remains countably
  atomic.
- Collapsing the tail to a cemetery changes the physical kernel and loses
  its branch cocycle/endpoint labels.  Renormalizing the retained branches
  changes the law and violates the full-mass requirement.

The same objection applies if one tries the forward deterministic quotient:
its finite-time law from a point is a Dirac mass.

### Exact full-mass model

The certificate includes the dyadic Gibbs--Markov quotient

```text
I=[0,1],   h_0(x)=x/2,   h_1(x)=(x+1)/2,
rho=1,     p_0=p_1=1/2.
```

This model has compact base, continuous weights, a weak-star continuous
kernel, exact full mass, and Lebesgue stationary measure.  At depth `n`, its
law from `x` is uniform on

```text
{(x+k)/2^n : 0<=k<2^n},
```

so the same support is an exact maximal-TV witness.  Thus compactness and
weak-star continuity do not bridge the gap to CDKM uniform ergodicity.

## 3. CDKM Theorem 4.1 hypothesis table

The exact source audited is Cai--Duraes--Klein--Melo,
*Holder continuity of the Lyapunov exponent for Markov cocycles via
Furstenberg's Formula*, arXiv:2212.00174v1.  Its PDF hash is

```text
e4a075ef0127b5860ac0533a4a16a6e7b78813320acbe69f07ceebb274819767
```

The paper defines uniform ergodicity as uniform exponential convergence in
total variation and uses it in Theorem 4.1.

| CDKM input | Exact pilot audit |
|---|---|
| compact symbol space | **conditional only**: a reference interval `I` would be compact, but the physical common-vertex quotient has not been built; the existing collision coding is countable/locally compact |
| weak-star continuous base kernel | **not certified** for the physical quotient; countable branch endpoints and grazing tails require a uniform summability/continuity proof |
| uniformly ergodic base kernel in TV | **rigorously false** for every exact countable inverse-branch kernel with non-atomic stationary density |
| Lipschitz `A:Sigma x Sigma -> GL(2,R)` | **not certified**: the full-mass billiard cocycle has unbounded return/homogeneity costs in its natural trivialization; no bounded Lipschitz compact representative or cohomological normalization has been produced |
| quasi-irreducibility | **open physically**: `J_g,J_w` are an SIP algebraic seed, but they are not yet two positive-weight transitions at one actual common vertex |
| simple top exponent | **open physically** for the same reason |

Even if the last two entries were closed, CDKM Theorem 4.1 proves Holder-test
mixing toward a stationary projective law.  It does not prove that the
stationary projective marginal is spatially Frostman.  That separate input
in the stationary-to-stopped bridge would still be missing.

One can pass to a finite symbolic factor whose transition matrix is primitive,
but that does not preserve the full physical object unless the collision
cocycle and Gibbs weights are proved to be locally constant on that finite
factor.  No such finite full-mass factor is present; the known coding is
countable and the derivative depends on the continuous collision point.

## 4. Why a compact truncation plus tail does not yield CDKM

Let `A_K` be a finite return/homogeneity core.

- Conditioning on `A_K` and renormalizing creates a different, generally
  negative-pressure subsystem.
- Sending the omitted mass to an absorbing cemetery preserves total mass but
  not the physical stationary law or the omitted projective matrices.
- Retaining the exact omitted destinations preserves the physical law but
  leaves the countably atomic finite-time kernel, so the TV obstruction is
  unchanged.
- Allowing `K=K(N)` at depth `N` produces an `N`-dependent family whose
  spectral constants can deteriorate with grazing rank.  CDKM Theorem 4.1 is
  a fixed-kernel theorem and supplies no uniform tail perturbation estimate
  for this diagonal limit.

Therefore there is no full-mass compact-truncation/Doeblin certificate of the
requested type.  A viable route must work in a weaker metric or directly on
a transfer-operator space; total-variation uniform ergodicity from point
states is the wrong topology for a deterministic/countable inverse-branch
quotient.

## 5. GKM independence cannot be replaced by adaptive Markov choice

The exact source audited is Gorodetski--Kleptsyn--Monakov,
*Holder regularity of stationary measures*, arXiv:2209.12342v1,
Theorems 2.6 and 2.8.  Its PDF hash is

```text
18d248b5f955d39679f04e57b30d29434587471fe78ee2d97f7907f22332a8d0
```

Theorem 2.6 iterates one fixed law on bi-Lipschitz maps.  Theorem 2.8 allows
laws `mu_1,...,mu_n` from a compact family, but the sequence is fixed in
advance and each map draw is independent of the current point.  In the
physical quotient, both the branch probabilities

```text
p_a(x)=rho(h_a x)|h_a'(x)|/rho(x)
```

and the next base point depend on the current state.  Conditioning on a
stopped history therefore produces an adaptive law, not a predeclared
non-i.i.d. sequence covered by Theorem 2.8.

### Exact adaptive counterexample on `P^1(R)`

Write a projective map as the Moebius action of its matrix.  Put

```text
A = [[3, 1], [1, 1]],      B = [[2,  0], [0, 1]],
C = [[1,-1], [1,10]],      D = [[2, -1], [0, 1]],
mu_0 = (delta_id+delta_A+delta_B)/3,
mu_1 = (delta_id+delta_C+delta_D)/3.
```

All four nontrivial maps are orientation-preserving hyperbolic projective
diffeomorphisms and have a uniform finite bi-Lipschitz moment.

For `mu_0`, a deterministic image would, because `id` belongs to the support,
be a probability invariant under both `A` and `B`.  Every invariant
probability of a hyperbolic projective map is supported on its two fixed
points.  The fixed set of `B` is `{0,infinity}`, while `A` fixes
`1+sqrt(2),1-sqrt(2)`; hence no common invariant probability exists.  Thus
`mu_0` has no deterministic images.  Likewise `D` fixes `{1,infinity}` and
the fixed points of `C` solve

```text
z^2+9z+1=0,
```

so `mu_1` also has no deterministic images.

This extends to a continuous compact law field.  In the affine chart put

```text
t(z)=z^2/(z^2+(z-1)^2),       t(infinity)=1/2,
mu_z=(1-t(z))mu_0+t(z)mu_1.
```

For every `0<=t<1`, the support contains `id,A,B`, so the same argument
excludes deterministic images; at `t=1`, use `id,C,D`.  Thus the whole
compact interval of mixtures satisfies the GKM assumptions uniformly.

Now use the current law `mu_z`.  Since `t(0)=0` and `t(1)=1`, exact
evaluation gives

```text
id(0)=0, A(0)=1, B(0)=0,
id(1)=1, C(1)=0, D(1)=1.
```

The two-point set `{0,1}` is invariant and its transition matrix is

```text
[[2/3,1/3],
 [1/3,2/3]].
```

Therefore `(delta_0+delta_1)/2` is an atomic stationary law.  If an adaptive
version of the GKM conclusion held with constants `alpha,C,kappa`, choose
`n` so large that `C kappa^n<1/4` and then a ball around `0` so small that
`C r^alpha<1/4`.  Its stationary mass is `1/2`, contradicting the claimed
strict bound.  This proves that the GKM hypotheses cannot simply be checked
state by state and then “Markovized”.

## 6. Latest-technology check

A targeted arXiv query on 2026-07-15 for the conjunctions
`Markov cocycle + Frostman` and
`stationary measure + Markov + Holder regularity` returned no direct result
extending GKM's energy contraction to adaptive place-dependent laws of the
form above.  The already audited 2026 results (Rush's i.i.d. Furstenberg
Frostman theorem and Thiam's finite-state Markov product spectral gap) do not
remove either obstruction:

- Rush requires one state-independent compactly supported matrix law;
- Thiam/CDKM-type product mixing does not supply spatial Frostman regularity;
- neither theorem constructs the full collision-SRB quotient or normalized
  stopped amplitudes.

## 7. Correct minimal positive route after this falsification

The new shortest nonvacuous route is not TV-Doeblin.

1. Construct the actual one-state full-mass quotient and its full branch,
   return, grazing, and density registry on the physical common vertex.
2. Prove a Doeblin--Fortet/spectral estimate in a weak or Holder/Wasserstein
   topology adapted to inverse branches, uniformly over the tail truncation.
3. Prove stationary projective Frostman regularity directly for the **joint
   place-dependent operator**, with an energy contraction that survives the
   correlation between the current state and the next branch law.  The
   adaptive counterexample shows that a joint no-atomic-graph/nonconcentration
   hypothesis is indispensable.
4. Feed that result to the already proved stationary-to-stopped smoothing
   bridge.
5. On the identical stopped tree, close the normalized amplitude moment and
   actual endpoint/projective carrier identity.

Steps 1, 3, and 5 remain open.  In particular this assault does not establish
`NST_phys`, `PPE_N`, or unconditional CM2.

## 8. Reproducibility

```bash
python3 -m py_compile \
  deliverables/cm2_gate2_markov_route_obstruction_cert.py
python3 deliverables/cm2_gate2_markov_route_obstruction_cert.py
python3 deliverables/cm2_gate2_markov_route_manifest_verifier.py --self-test
python3 deliverables/cm2_gate2_markov_route_manifest_verifier.py
sha256sum -c \
  deliverables/cm2-gate2-markov-kernel-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The live manifest verifier intentionally exits `2`, because the physical
quotient, physical projective Frostman theorem, amplitude ledger, and
same-carrier endpoint identity are not certified.

## 9. Final Gate-2 status

| Item | Status |
|---|---|
| exact actual-kernel formula, conditional on a quotient | **proved previously** |
| CDKM uniform ergodicity of the reverse-branch base | **rigorously false** |
| full-mass compact truncation with physical Doeblin minorisation | **rigorously impossible in TV** |
| GKM 2.6/2.8 for fixed/predeclared independent laws | **applicable only to artificial benchmarks** |
| extension under adaptive state-dependent law from the same hypotheses | **rigorously false** |
| physical common-vertex quotient and tail registry | **open** |
| weak-topology joint operator gap | **open** |
| stationary spatial Frostman for the physical Markov cocycle | **open** |
| normalized stopped amplitude and endpoint typing | **open** |
| physical Gate 2 | **NOT CERTIFIED** |
