# CM2 Gate 2: actual full-mass quotient and projective-tail assault

Date: 2026-07-15 (Asia/Shanghai)  
Scope: Gate 2 physicalisation after the true two-graph common-vertex
certificate; frozen v51/v52 and the shared research log are not edited  
Verdict: **a no-renormalisation finite-core theorem and the exact missing
tail statistic are proved; the physical quotient and Gate 2 remain OPEN /
NO-GO**

## 1. Executive result

The new 500-bit Krawczyk certificate materially changes the Gate-2 input:
there is now an explicit regular point

```text
q in T^10 W^u_loc(QNL) intersection T^-14 W^s_loc(connector)
```

and the intersection is transverse.  This retires the former
eigentangent-only warning.  It does **not** produce a positive-width return
rectangle.  In particular, a single transverse point has collision-SRB mass
zero and does not define a reference unstable interval, a full return
partition, or positive physical weights for the pilot loops.

After this report's first draft, the companion full-cross certificate also
closed a positive-width directed QNL-to-connector transition rectangle and
its reversible opposite strip.  That update is incorporated here.  It still
does not produce a closed dwell/return loop or a one-state Young return base.

This assault proves two new statements which make the remaining obstruction
precise.

1. **Finite core plus tail can be used without renormalisation.**  If the
   unnormalised physical subkernel on a growing finite branch core has one
   uniform two-copy energy drift, then the exact full physical law has the
   same small-ball bound plus the true probability of ever selecting an
   omitted branch.  No factor `1/(1-epsilon_B)` and no survivor-conditioned
   law occurs.

2. **A marginal branch tail is not the missing energy estimate.**  Even a
   finite tail of arbitrarily small positive mass, with uniform
   co-Lipschitz bounds and all branch-loss moments, can contain two distinct
   projective maps whose images coincide at different inputs.  That single
   cross pair makes the uniform truncated-Riesz drift impossible.  The
   missing physical datum is an off-diagonal projective near-collision
   estimate, or a block criterion which replaces it.

The audit also gives the exact candidate countable alphabet, reverse kernel,
projective maps, tail complexity, stopped prefix antichain, and amplitude
registry which would be used after a rectangle is declared.  At present all
of those are schemas rather than instantiated pilot objects.  The earliest
hard dependency is now exact:

```text
true point q                                  CERTIFIED
directed four-face transition strips          CERTIFIED
closed dwell/return loop                      NOT CERTIFIED
q-anchored one-state Young/Gibbs base         NOT INSTANTIATED
countable branch/weight/projective registry   NOT INSTANTIATED
```

Consequently Gate 2 is not promoted.

## 2. What the new common vertex proves, and what it cannot prove

The certificate `cm2_gate1_true_graph_krawczyk_cert.py` proves all of the
following on the declared 10+14 first-hit words:

```text
actual W^u_loc(QNL) source                         yes
actual W^s_loc(connector) source                   yes
true two-graph Krawczyk inclusion                  yes
det D F = 6.82e14 +/- 7.16e11 > 0                 yes
all 24 collisions and first-hit margins            yes
directed four-face full crossing about the root    yes
reverse inherited transition strip                 yes
closed dwell/return loop                            no
closed common-vertex transported loop              no
transported four-wedge twisting                    no
```

The determinant is the wedge of the two **different carrier tangents** used
in the matching problem.  It proves transversality of the two invariant
manifold images.  It is not the endpoint wedge `dX wedge dY` on one PPE
carrier.

To obtain a branch of a return quotient one needs open strips.  The new
full-cross certificate supplies such strips for the directed 24-collision
QNL-to-connector transition and, by reversibility, its inherited opposite
transition.  It does not join their off-centre endpoints by one finite
shadowing/dwell word, so the two strips are not yet a first-return branch of
one rectangle.

If `Lambda` is a product rectangle and `Lambda_a` is a return strip, the statement

```text
T^R_a(Lambda_a) u-crosses Lambda
```

contains four strict face inequalities and persists on a positive-width
family of unstable leaves.  The separate full-cross certificate now supplies
the declared widths and strict face margins.  The remaining objection is no
longer continuity or four faces: it is the absent closed return loop and
Young base.

Lima--Obata--Poletti Lemma 5.1 gives a second clean heteroclinic connection
existentially and hence an existential clean basic set.  That finite basic
set is not a full collision-SRB object: its unstable conditional is a
horseshoe Gibbs law and the set has zero collision-SRB mass.  It can supply a
topological gate seed, but it cannot be substituted for a full-mass Young
quotient or be conditioned and renormalised.

## 3. Exact candidate physical quotient

This section fixes the labels which must be produced.  It does not assert
that the required rectangle currently exists.

Let `Lambda` be a declared homogeneous Young return rectangle containing a
positive-width gate about `q`, let `I` be one reference unstable interval,
and let `pi^s:Lambda -> I` be stable holonomy.  For a point before its first
return to `Lambda`, the **dynamical** return record is

```text
R       return time;
omega   complete solid-collision/lift word;
k       complete homogeneity-strip word.
```

The countable alphabet is then unambiguously

```text
A = {connected components Lambda_a of
     {first return R, word omega, homogeneity word k}
     which s-cross Lambda and whose image u-crosses Lambda}.
```

It is countable because `R` is integral, the collision/lift and homogeneity
alphabets are countable, and connected components are indexed separately.
Orientation, physical-face component, entrance/exit context, and recovery
are a separate countable **fiber mark** `ell`; they are not silently promoted
to inverse branches.  Such a promotion could cut a return strip into pieces
which no longer have full image.  This is exactly the marked-full-branch
discipline of v52.

Writing `I_a=pi^s(Lambda_a)`, the quotient return and inverse branches are

```text
Fbar:I_a -> I,               h_a:I -> I_a.
```

If the quotient collision-SRB conditional is `rho(x) dx`, invariance forces
the exact reverse weights

```text
p_a(x) = rho(h_a x) |h_a'(x)| / rho(x),
sum_a p_a(x) = 1.
```

For a word `w=a_1...a_n`, density cancellation gives

```text
p_w(x) = rho(h_w x) |h_w'(x)| / rho(x).
```

The global collision density `cos(phi) dr dphi` does not by itself give this
`rho`: stable projection to `I` inserts the stable-holonomy and chart
Jacobians.  A reference interval, its holonomy, and upper/lower density and
distortion bounds therefore must be recorded.

Let the transported derivative of branch `a`, from `y=h_a(x)` to `x`, in
one fixed arclength--momentum trivialisation on the same base, be

```text
M_a(y) = [[a_a(y), b_a(y)], [c_a(y), d_a(y)]].
```

There are two legitimate but different projective directions.  Forward
tangent transport is

```text
Phi_a^+(x,z)
  = (c_a(h_a x)+d_a(h_a x) z)
      /(a_a(h_a x)+b_a(h_a x) z),
```

whereas a reverse/pullback tangent chain uses the same slope formula with
`M_a(h_a x)^(-1)`.  The stopped PPE construction must declare which state
`z` represents and use that direction everywhere; the two may not be
interchanged after taking laws.  Entrance and exit holonomies belong inside
this same matrix record.  A periodic-orbit matrix in its own trivialisation
is not `M_a`.

A useful dynamical tail complexity is

```text
c_dyn(a) = R_a + B_a,
```

where `B_a` is maximal grazing/homogeneity rank.  The physical finite core
and its exact one-step omitted probability would be

```text
A_B       = {a:c_dyn(a)<=B},
epsilon_B = sup_x sum_{a notin A_B} p_a(x).
```

The marked amplitude/endpoint ledger separately needs a joint moment of
`c_dyn(a)+C^-+C^++recovery` under `(a,ell)`.  That marked moment does not
alter `p_a` or the full-image dynamical alphabet.

This is the requested full-mass alphabet/kernel/projective/tail dictionary.
No `Lambda`, `I`, `Lambda_a`, `rho`, `M_a`, or numerical `epsilon_B` with
these common labels is currently present in the pilot deliverables.

## 4. Audit of the v52 countable-IFS claims

The countable-IFS section of v52 contains correct conditional reductions,
but it does not instantiate the preceding dictionary.

| v52 layer | Exact logical status after the new vertex |
|---|---|
| Marked full-branch quotient | Conditional proposition: it starts with a Young rectangle and full return partition.  Directed transition strips now exist at `q`, but no closed return rectangle/base is selected. |
| Collision-SRB equilibrium potential | Actual: LOP Lemmas 5.2--5.3 identify the geometric equilibrium potential and a countable coding. |
| One-state return base and exponential tail | Not supplied by LOP 5.2--5.3 and not instantiated in the pilot. |
| Central amplitude moment | Conditional on an exponential return moment, a compact homogeneity core, and a complete physical insertion/recovery registry. |
| Return--maximal-grazing moment | Conditional on a chosen Young base and its exponential return tail. |
| Fixed-gate hitting/context moment | Conditional on a genuine full-branch gate cylinder with a Gibbs lower bound.  The directed strip is certified, but it is not yet a closed return cylinder in one Young base. |
| LPS light tail | Conditional consequence of the preceding joint moments; no numerical pilot branch sum is present. |
| Actual `p_a` and word telescoping | The formula and algebra are proved, but the branch/density registry is absent. |

Thus the new common point advances the geometry immediately before the
fixed-gate hypothesis.  It does not change any conditional premise into a
full-mass quotient.

## 5. A finite-core theorem with no truncation renormalisation

Let `P` be the exact physical kernel and let `A_B` be a finite branch core.
Define the **unnormalised** retained subkernel

```text
P_B f(u) = sum_{a in A_B} p_a(u) f(T_a u).
```

No division by `sum_{a in A_B}p_a(u)` is made.  Put

```text
epsilon_B = sup_u sum_{a notin A_B}p_a(u).
```

### Theorem 5.1 (full-law transfer from an unnormalised core)

For `0<alpha<=1` and `0<r<=1`, let

```text
V_r(u,v)=max(r,|pi(u)-pi(v)|)^(-alpha).
```

Suppose, with constants independent of `B`,

```text
(P_B tensor P_B)V_r(u,v)
   <= kappa V_r(u,v)+C_0,          0<kappa<1.               (5.1)
```

Let `nu_n` be the projective law of the exact full kernel from one point.
Then every interval `J` of length `r` satisfies

```text
nu_n(J)
 <= {kappa^n+C_0 r^alpha/(1-kappa)}^(1/2)
       + n epsilon_B.                                      (5.2)
```

#### Proof

Let `nu_n^B` be the subprobability of paths whose first `n` labels all lie
in `A_B`.  Two independent retained copies are governed by
`P_B tensor P_B`.  Iterating (5.1), starting both copies at the same state,
gives

```text
E[V_r(U_n,V_n); both paths retained]
 <= kappa^n r^(-alpha)+C_0/(1-kappa).
```

If both projective coordinates lie in `J`, their energy is `r^(-alpha)`;
hence

```text
nu_n^B(J)^2
 <= kappa^n+C_0 r^alpha/(1-kappa).
```

At each step the exact conditional probability of a label outside `A_B` is
at most `epsilon_B`, so the physical probability of any omitted label is at
most `n epsilon_B`.  Adding it proves (5.2).  There is no conditioning on
survival and no changed Gibbs potential.

If

```text
epsilon_B <= C exp(-cB),       B_n=ceil(lambda n),
```

the last term is `O(n exp(-c lambda n))`.  This is the clean admissible form
of a growing-core tail.  The two fixed pilot maps alone cannot be used in
this theorem: their omitted physical mass has not been bounded and their
fixed subsystem is known to have negative relative pressure.

## 6. Exact full-countable pair-energy criterion

For branch maps `Phi_a` suppose

```text
|Phi_a(u)-Phi_a(v)| >= ell_a |pi(u)-pi(v)|,
0<ell_a<=1.
```

Define the same-label coefficient

```text
S_alpha = sup_(u,v)
  sum_a p_a(u)p_a(v) ell_a^(-alpha)                         (6.1)
```

and the off-diagonal branch-image energy

```text
C_alpha = sup_(u,v,r)
  sum_(a!=b) p_a(u)p_b(v)
  max(r,|Phi_a(u)-Phi_b(v)|)^(-alpha).                      (6.2)
```

Then

```text
(P tensor P)V_r <= S_alpha V_r+C_alpha.                    (6.3)
```

Therefore `S_alpha<1` and `C_alpha<infinity` close the full countable drift
directly.

The same-label part has a useful physical reduction.  Suppose two declared
branches each have pointwise weight at least `eta>0`, and suppose for some
`delta>0`

```text
M_delta = sup_u sum_a p_a(u)ell_a^(-delta) < infinity.
```

Every individual branch weight is then at most `1-eta`.  Cauchy--Schwarz
and the Lyapunov moment inequality give, for `0<alpha<=delta`,

```text
S_alpha
 <= (1-eta) M_delta^(alpha/delta).                          (6.4)
```

Hence the same-label term is strictly contracting for sufficiently small
`alpha`.  Once a true common full-cross supplies two positive Gibbs hazards,
and the return/grazing ledger supplies `M_delta`, this part is not the main
obstruction.

The genuinely new statistic is (6.2).  A sufficient form is a uniform
off-diagonal small-ball estimate: for some `beta>alpha`,

```text
sum_(a!=b) p_a(u)p_b(v)
  1{|Phi_a(u)-Phi_b(v)|<=t}
 <= C t^beta.                                               (6.5)
```

Layer-cake integration makes (6.2) finite.  No return-time or co-Lipschitz
moment alone implies (6.5).

## 7. Exact counterexample: marginal tail moments do not close the drift

On `K=[0,1]` take the four affine projective maps

```text
Phi_g(z)  = z/4,                weight 2/5,
Phi_w(z)  = 3/4+z/4,            weight 2/5,
Phi_t0(z) = 1/3+z/6,            weight 1/10,
Phi_t1(z) = 1/4+z/3,            weight 1/10.
```

All maps preserve `K`, all are orientation-preserving and co-Lipschitz by
`1/6`, the tail mass is only `1/5`, and the two core images have gap `1/2`.
Moreover

```text
sum_a p_a^2 = 17/50,
6 * 17^20 < 50^20,
```

so the same-label coefficient is strictly below one at `alpha=1/20`.

Nevertheless

```text
Phi_t0(0)=Phi_t1(1/4)=1/3.
```

Use the same `alpha=1/20`, take `u=0`, `v=1/4`, and put `r=n^-20`.
The input energy is the fixed number `4^(1/20)<2`, while this one ordered
tail cross pair contributes

```text
(1/10)(1/10) r^(-1/20) = n/100.
```

For any proposed fixed `kappa<1,C_0`, choose
`n>100(2+C_0)`.  The drift inequality fails.  The example is finite,
so it has every marginal label, return, and branch-loss moment.  It proves
that the missing cross-image statistic cannot be replaced by the schematic
tail moment already present in v52.

This does not prove that the physical billiard drift is false.  It proves
that the current physical inputs are logically insufficient to certify it.

## 8. Actual stopped antichain audit

Once a full inverse system exists, the canonical scale-`sigma` prefix
antichain is

```text
S_sigma={w:diam(I_w)<=sigma<diam(I_parent(w))}.              (8.1)
```

It is countable, prefix-free, and measurable.  If inverse cylinders shrink
to points almost surely, it carries full mass under the exact word kernel.
This closes only the abstract antichain algebra.

It does not imply the two-sided native comparison required by
`NST_phys`.  In the exact Lebesgue full-branch model

```text
h_n([0,1])=[2^-n,2^-(n-1)],       p_n=2^-n,
```

at scale `sigma=2^-m`, all first children with `n>2m` have length below
`sigma^2`; their exact total mass is

```text
sum_(n>2m)2^-n = 2^-2m = sigma^2.
```

Thus even a perfectly normalized full-branch quotient needs a named
overshoot cemetery or a further physical refinement before a uniform lower
scale bound is true.  For the billiard pilot the needed return/grazing tail
and homogeneous continuation have not been instantiated on a declared
quotient, so (8.1) remains a schema and `NST_phys` remains open.

## 9. Same-carrier endpoint audit

On one declared carrier `gamma(t)`, actual endpoint maps `X(t),Y(t)` and the
actual tangent coordinate `z` satisfy the exact algebra

```text
dY(1,z)/dX(1,z)
  = (Y_1+Y_2 z)/(X_1+X_2 z),

d/dz = (Y_2 X_1-Y_1 X_2)/(X_1+X_2 z)^2.
```

The new common-vertex determinant does not instantiate these symbols.  It
compares

```text
D_t(T^10 gamma_QNL)     and     D_u(T^-14 gamma_connector),
```

which are two different carriers meeting at one point.  The physical PPE
record still needs one carrier, both actual endpoint maps on every retained
continuation, the transported projective tangent from the same directed
branch matrix `M_a`, a denominator bound, and the nonzero endpoint wedge.  None of
those records can be inferred from equality at `q` or from equality in law.

Therefore the local common-vertex wedge is certified, while
`SAME_CARRIER_PHYSICAL_ENDPOINT_IDENTITY` remains open.

## 10. Amplitude registry audit

Two positive algebraic layers are already available.

1. The finite-operation construction

   ```text
   J_PPE = disjoint_union_(k>=0) J_0 x O^k
   ```

   is a standard-Borel registry whenever the generator set, operation
   alphabet, evaluations, and record-to-word map have been declared.

2. On one clean interval, a density floor plus relative scaled Holder
   control gives a parentwise moment of `A/Z_A`.

Neither layer supplies the actual list.  For the q-anchored quotient one
would have to freeze, before the final target is selected, every generator
and every operation used by

```text
branch restriction; collision and chart Jacobian;
stable holonomy; coarea/face velocity; positive/negative split;
recovery; endpoint/test lift; owner handler; cemetery continuation.
```

The current pilot has local formulas for several clean components, but no
one master occurrence tree and no exhaustive record-to-word map.  It also
lacks the conditional moment of the resulting scaled distortion mark over
all return/homogeneity/context tails.  Hence neither the actual registry nor
the global normalized moment is certified.

## 11. Minimal obstruction and next certificate

The shortest physical continuation is now a concrete finite-to-countable
package.

1. Join the certified forward/reverse full-cross strips by a finite
   dwell/shadowing word, validate the resulting closed return rectangle, and
   record one reference unstable interval `I`.
2. Generate the first-return components with the exact labels in Section 3,
   including all omitted components.  Compute `rho`, `h_a`, `p_a`, and the
   transported directed matrices `M_a` in one trivialisation.
3. Choose a growing complexity core `A_B` and certify the **unnormalised**
   subkernel drift (5.1), together with the exact physical tail
   `epsilon_B`.  Do not replace it by a normalized survivor kernel.
4. Either certify the off-diagonal branch-image bound (6.5) or use a
   multi-step/block energy inequality which explicitly handles branch-image
   crossings.  Marginal return/grazing moments are insufficient.
5. Generate the prefix antichain, overshoot cemetery, endpoint carrier
   records, and exhaustive amplitude operation words on these same labels.

Until item 1 is complete, the alphabet itself cannot be instantiated at the
certified directed full-cross.  Until item 4 is complete, even an abstract Young quotient
and its standard tail do not imply the new pair-energy hypothesis.

## 12. Reproduction and stopping line

Run

```bash
python3 -m py_compile \
  deliverables/cm2_gate2_full_mass_tail_cert.py \
  deliverables/cm2_gate2_full_mass_tail_manifest_verifier.py
python3 deliverables/cm2_gate2_full_mass_tail_cert.py
python3 deliverables/cm2_gate2_full_mass_tail_manifest_verifier.py --self-test
python3 deliverables/cm2_gate2_full_mass_tail_manifest_verifier.py
sha256sum -c \
  deliverables/cm2-gate2-full-mass-tail-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The positive certificate exits zero.  The live physical manifest exits two
by design and ends with

```text
PHYSICAL_GATE2: NOT_CERTIFIED
```

Final status:

```text
TRUE_COMMON_VERTEX_POINT: CERTIFIED
DIRECTED_FULL_CROSS_TRANSITION_STRIPS: CERTIFIED
CLOSED_DWELL_RETURN_LOOP: NOT CERTIFIED
UNNORMALISED_FINITE_CORE_TRANSFER: PROVED
MARGINAL_TAIL_SUFFICIENCY: RIGOROUSLY FALSE
Q_ANCHORED_FULL_MASS_QUOTIENT: NOT CERTIFIED
FULL_COUNTABLE_PAIR_ENERGY: NOT CERTIFIED
ACTUAL_NST_AND_AMPLITUDE_REGISTRY: NOT CERTIFIED
SAME_CARRIER_ENDPOINT_TYPING: NOT CERTIFIED
GATE_2_PHYSICAL: OPEN / NO-GO
```
