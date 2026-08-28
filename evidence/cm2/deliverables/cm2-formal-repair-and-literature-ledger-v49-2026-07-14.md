# CM2 v49 formal-repair and literature ledger

Date: 2026-07-14 (Asia/Shanghai)

Scope: hypothesis-driven follow-up to the hostile review of frozen v48.  This
ledger distinguishes proved statements, exact algebraic reductions, and still
open research gates.  It does not promote the fixed-section pilot to the
standard full-boundary collision-map theorem.

## Formal repairs now implemented in the v49 working source

- `PAIR_SAFE_REFERENCE` now includes a uniform retained-mass floor on every
  actual frozen parent.  `CLOCK_PROB_W <= C exp(-c N_time)` is explicitly not
  used to infer that floor at bounded `N_time`.
- The global H3 theorem call now states the survivor floor explicitly, and the
  PPE-to-pair theorem assumes the floor itself rather than an inapplicable
  asymptotic lemma.
- The occurrence-kernel compatibility condition is a probability-one equality
  set, not a topological-support assertion on a merely standard-Borel space.
- The incidence owner partition is modulo `overline M^q`-null sets, the measure
  that actually lives on the incidence graph.
- The zero-mass/null-proposal conclusion is assigned to FS4; FS3 supplies only
  the positive-mass normalized hereditary estimate.
- Translation-rate margins use a weighted parentwise exponent
  `Theta_PPE^{W,tr}`.  If the only transfer is Holder/KRH, no exponent larger
  than `Theta_PPE^{tr}/p_W'` is inserted.
- The deterministic path is required to remain in the admissible center ball
  uniformly in the whole parameter interval.
- The impact/coarea lemma now selects an incoming first-hit root in a fixed
  torus lift and a typed time interval.  It does not sum the entry and exit
  roots.
- The fixed-section theorem now calls a fixed-phase assembly theorem whose
  quantified object is `F_c`.  Transfer to the standard full-boundary
  collision map is isolated as the separate `SECTION_FULL_CM2` theorem.

## New proved pilot primitives

For the explicit path `c(s)=(s,0)`, `|s|<1/400`, use the left transparent wall
and

```
|y| < 1/100,
|w| < 1/100,
q_0 = (-1/2,y),
u = (1,w)/sqrt(1+w^2).
```

Exact rational estimates prove:

- the entire unit clean-pass segment remains more than `97/200` from every
  gray-disk lift, hence lies in the interior of the fixed section;
- the normalized line-to-white-center distance is at most `601/6400`;
- the incoming root is the unique root in `(1/4,1/2)` and is the physical first
  collision; the outgoing root is larger than `1/2`;
- `n.u < -99/100` and `n.e_1 < -49/50`;
- the cylinder has strictly positive `mu tensor ds` mass, and its impact-time
  mark has constant sign with `49/50 < partial_s t < 100/99`.

The exact scripts `cm2_fixed_section_geometry_cert.py` and
`cm2_fixed_section_impact_cert.py` certify the rational inequalities and the
polynomial implicit-derivative identities.

## Bounded-inducing reduction obtained from Stenlund's construction

Stenlund, Sections 2.1--2.4, defines the fixed section `M`, the enlarged section
`M* = M disjoint_union W`, and a return depth `n_c in {1,2}`.  A point of `W`
returns to `M` at its next enlarged-section iterate.  Therefore, with

```
P_c^* = [ A_c  B_c ]
        [ C_c   0  ],
```

the fixed-section transfer operator satisfies the exact identity

```
P_c = A_c + B_c C_c.
```

Its finite difference quotient is exactly

```
Delta_s P = Delta_s A + (Delta_s B) C_0 + B_s (Delta_s C).
```

This closes the algebraic bounded-inducing step and shows that no infinite
renewal series or derivative of an unrecorded stopping time is needed.  It
does not prove convergence of the three block currents, and it does not
transfer CM2 to the standard collision map because the enlarged section still
contains transparent-wall returns.

## Targeted literature audit through 2026-07-14

### Stenlund, arXiv:1210.0902 / CMP 325 (2014)

Usable: fixed section independent of the white center, common invariant
probability, reversibility, free-zone one-white-hit property, and the exact
depth-`{1,2}` enlarged-section representation.

Not supplied: parameter differentiation of the entry/exit blocks, a physical
moving current, weighted PPE, or transfer to CM2 of the standard full-boundary
collision map.

### Canestrari, arXiv:2604.19671v2 (2026)

Definition 5.3 and Proposition 4.4 start from an initial regular standard
family/measure and propagate it.  The long-side recovery and normalized
boundary recursion are relevant only after the moving flux source has been
proved to be such a family.

Not supplied: construction of an initial regular family from this moving-face
coarea current, nor the hereditary rare-cell estimate on every stopped law.

### Galatolo--Lucarini, arXiv:2603.19509v3 (2026)

Theorem 11 develops a global-resolvent response theorem on a fixed sequence
space of transfer operators under loss of memory and differentiability
assumptions.

Not supplied: identification of two different Poincare sections, singular
billiard boundary currents, or a section-to-standard-collision CM2 theorem.

### Friedland, arXiv:2606.24823 (2026)

The disk-growth theorem gives a modular proof of the measurable
Turan--Nazarov inequality with the sharp algebraic exponent for finite-order
exponential polynomials.

Potential use: the scalar sublevel step if a terminal billiard phase can first
be represented with uniformly bounded exponential order and controlled disk
growth.

Not supplied: that representation, the all-depth billiard jet, weighted
parentwise amplitudes, or survivor normalization.

### Demers--Liverani, arXiv:2606.10155 (2026), and sequential/random work

Usable: current uniform hyperbolic, growth, cone, and loss-of-memory packages.
The review confirms that conditioning on small sets and general aperiodic
Lorentz-gas memory loss remain delicate.

Not supplied: the four gates combined here (moving block current, flux-family
entry, hereditary stopped-law `Z`, and all-depth weighted PPE).

## Remaining research gates, in shortest order

1. Prove typed DQ convergence for `A_c`, `B_c`, and `C_c` on a finite recorded
   first-hit atlas, including entry/exit orientations, tangency boxes, and
   exact occurrence/source current matching.
2. Push the nonzero first-hit current to unstable curves and prove an initial
   regular standard-family estimate with a hereditary `W Z^chi` bound on every
   global, shallow, and stopped-deep law.
3. Establish an invariant all-depth terminal jet cone and the exhaustive
   weighted PPE2--PPE4 registry on the identical stopped tree.
4. Prove `SECTION_FULL_CM2`, including observable lifts, centering, roof/return
   corrections, and absolute CM2 summability.  CM2 is not assumed invariant
   under a parameter-dependent change of Poincare section.

No source located through 2026-07-14 closes any of these four gates as a
single theorem.  The v49 changes therefore close formal calls and add genuine
base primitives while leaving the remaining research theorems explicit.
