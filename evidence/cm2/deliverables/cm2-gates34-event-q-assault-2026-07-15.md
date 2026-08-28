# CM2 Gates 3–4 direct assault: global event inventory and same-occurrence `q`

Date: 2026-07-15  
Scope: rational two-disk pilot, with the direct standard solid-boundary section
`N=G\sqcup W` as the reduced route.  The frozen v51/v52 manuscript files were
read but not edited.  The shared research log was not edited.

## Decision

- **Gate 3 — NOT CERTIFIED.**  A new rigorous certificate gives
  `tau_max<3` and the complete conservative target-lift universe
  `G,W: [-4,4]^2`; the exact one-target tangency submersion is also valid.
  An exact eight-cell dominant-coordinate source cover is now recorded.
  There is still no chart-specific candidate table, no selected first-hit
  time table, no complete pair/triple incidence table, and no global
  DQ/scalar-current bridge.
- **Gate 4 — NOT CERTIFIED.**  The current positive local construction records
  `i_ent` and `i_exit` as two additive occurrences with separately defined
  envelopes.  It does not give two nonadditive representations of one
  occurrence, and it has neither the exact single-charge
  `q=max(C_forward,C_reverse)m` nor bidirectional recovery moments on that
  same `q`.

The fail-closed evidence snapshot and verifier are:

- `deliverables/cm2-gates34-event-q-manifest-2026-07-15.json`;
- `deliverables/cm2_gates34_manifest_verifier.py`;
- `deliverables/cm2_standard_section_horizon_lift_cert.py`;
- `deliverables/cm2-gates34-assault-manifest-2026-07-15.sha256`.

The verifier passing its synthetic structural self-test means only that its
coverage logic is internally consistent.  The actual evidence snapshot exits
with status 2 and reports both gates as `NOT_CERTIFIED`.

## 1. Audit of the two existing standard-section certificates

### 1.1 What the geometry certificate proves

`cm2_fixed_section_geometry_cert.py` proves, by exact rational comparisons,

\[
 \bar R=\frac9{25},\qquad R=\frac4{25},\qquad
 \varepsilon=\frac1{200},
\]

the no-overlap, finite-horizon blocking and free-zone inequalities used in
the pilot.  In particular, the shortest gray–white diagonal surface gap has
the certified lower bound

\[
 \tau_{\min}>\frac{1821}{10000}.
\]

This is enough for a lower free-flight margin.  The geometry script itself
does **not** output an upper free-flight number `tau_max`; qualitative finite
horizon alone is not a machine-checkable lift enumeration.  The next
certificate supplies the missing numerical layer independently.

### 1.2 New uniform horizon and target-lift certificate

The actual moving white disk contains, for every allowed center displacement,
the fixed nominal core

\[
 R_{W,\mathrm{core}}=\frac4{25}-\frac1{200}=\frac{31}{200}.
\]

`cm2_standard_section_horizon_lift_cert.py` makes an exact dyadic cover of

\[
 [0,1]^2\times(\mathbb R/2\pi\mathbb Z)
\]

and refines it adaptively.  On each of 35,024 final boxes, 160-bit Arb
arithmetic verifies one fixed rational time `t in [3/4,3]` and one fixed gray
or nominal-white-core lift for which the entire ray box lies strictly inside
that disk at time `t`.  The deepest binary refinement is 14 and 72 distinct
disk witnesses occur.

Because

\[
 \frac34>2\max\left\{\frac9{25},\frac{31}{200}\right\}
 =\frac{18}{25},
\]

the witness cannot merely be the same disk still containing the starting
point.  A physical ray starting outside the obstacles therefore crosses a
future obstacle boundary strictly before time 3.  Since every actual white
disk contains its fixed core,

\[
 \boxed{\tau_{\max}<3}
\]

holds uniformly on the full displacement ball, not only on the narrower
one-parameter path.

For a source lift in `[0,1]^2`, every hit point before time 3 is
coordinatewise in `[-3,4]`.  Exact radius/displacement padding then proves
that all possible gray and white lattice indices lie in the deliberately
conservative finite boxes

\[
 (i,j)\in[-4,4]^2.
\]

This closes the numerical horizon/lift-universe subgate.  It does not say
which of the 162 declared target lifts is admissible from a particular source
chart, which root is first, or how event currents match.

### 1.3 Exact source phase cover

For each of `G` and `W`, split the unit normal circle by its dominant
coordinate.  Diagonal ties are assigned to the east/west cells:

\[
 \begin{array}{ll}
 E:\ n_x\ge |n_y|,&W:\ -n_x\ge |n_y|,\\
 N:\ n_y>|n_x|,&S:\ -n_y>|n_x|.
 \end{array}
\]

The identity `n_x^2+n_y^2=1` implies that the subordinate coordinate has
absolute value at most `1/sqrt(2)`.  Thus each cell is one radical graph
`n=(+/-sqrt(1-t^2),t)` or `n=(t,+/-sqrt(1-t^2))`.  With
`p=sin(phi) in (-1,1)`, the fixed gauge is

\[
 q=a_{\rm src}(s)+R_{\rm src}n,\qquad
 u=\sqrt{1-p^2}\,n+p\,n^\perp.
\]

The resulting eight chart rows cover the interior of both solid-boundary
phase components with disjoint coverage cells (apart from assigned seams).
The four `p=+/-1` component boundaries remain explicitly registered genuine
grazing strata.  What is missing is the certified candidate-target subset of
the 162-lift universe for each chart.

### 1.4 What the tangency certificate proves

For a source point `q`, outgoing unit vector `u`, target center `a` and target
radius `R_k`, put

\[
 w=u^\perp\!\cdot(a-q),\qquad
 \Delta_k=R_k^2-w^2.
\]

At a selected forward tangency, with
`ell=u\cdot(a-q)>0`, the exact identity is

\[
 |\partial_\varphi\Delta_k|=2R_k\ell.
\]

The script correctly combines `R_min=4/25` and the certified surface gap to
obtain

\[
 |\partial_\varphi\Delta_k|>
 \frac{1821}{31250}=0.058272.
\]

Thus a **specified physical forward target tangency** is a regular event
face.  The premise “specified physical forward target” already requires the
missing global work.  In particular the script does not certify:

1. which source component/chart contains `q`;
2. that the candidate is not the zero-time copy of the source obstacle;
3. which target lift `a` is being used and that all possible lifts were
   listed;
4. the incoming positive root and its occurrence time;
5. that this root precedes every competing collision;
6. a face label, physical trace, coarea coefficient, polarity or owner;
7. any pair/triple event intersection;
8. the DQ coefficient or its physical/source scalar-current identity.

The script itself therefore correctly prints
`GLOBAL_EVENT_DQ_AND_MATCHING: NOT CERTIFIED`.

### 1.5 A useful global algebraic reduction, but not an inventory

After exact lift deduplication, two distinct Euclidean target circles cannot
give coincident tangency hypersurface germs on a regular source chart.  If
they did, a one-dimensional family of oriented lines would be tangent to both
circles.  Two distinct circles have only finitely many common tangent lines
(at most four), a contradiction.  Consequently a genuine coincident factor
can only come from an unremoved duplicate representation of the same circle
or from a change of source/lift chart.

This removes one class of unknown common factors on the direct `N` route.  It
does not enumerate isolated common tangencies, prove the required coefficient
envelope there, or remove triple/higher incidences.  It also does not replace
the exact duplicate-trace cancellation at overlaps of quotient charts.

## 2. Gate 3: the required global manifest

The manifest is fixed before a parameter, depth, frequency, final test, or
product-time orientation query is selected.  Its finite universe is built in
this order.

### 2.1 Horizon and source atlas

1. Record exact `tau_min` and a certified numerical `tau_max` uniform on the
   full parameter window.  This item is now closed with `tau_max<3`.
2. Cover both circular source components `G` and `W` in the fixed
   arclength–angle gauge by a finite chart list with disjoint interiors and
   explicitly recorded overlaps.  The eight dominant-coordinate cells above
   close this item for the phase interior; `p=+/-1` stay as named grazing
   boundary strata.
3. On every source chart choose one Euclidean lift and record its domain,
   physical quotient map, outgoing convention and phase-boundary labels.
4. Derive from `tau_max` the complete finite list of target circles/lifts
   reachable before the next collision.  This item is now closed by the
   certified conservative `[-4,4]^2` family boxes; chart-specific pruning is
   still part of the event table.

### 2.2 One row per candidate event

For each `(source_chart,target_lift)` candidate, one row must contain:

| field | required content |
|---|---|
| `event_equation` | the exact `Delta_k` or its square-free factor |
| `selected_root` | incoming root, with a certified positive interval |
| `occurrence_time` | the physical time attached to that root |
| `first_hit_certificate` | strict comparison with every competing candidate |
| `face_label` | immutable globally unique face/word/lift label |
| `submersion_certificate` | nonzero margin on the admissible zero set |
| `physical_trace` | the actual one-sided collision-map traces |
| `coarea_coefficient` | exact derivative/coarea scalar with sign |
| `polarity`, `owner` | immutable current-decomposition fields |
| `m_id`, `q_id` | exact coefficient and dominating-envelope records |
| `occurrence_id` | single physical incidence identity |
| `scalar_current_certificate` | restrictionwise physical/source equality |

The root and first-hit inequalities are not cosmetic.  Without the selected
interval a delta/coarea formula counts both line–circle roots; without all
competitor comparisons an algebraic tangency may occur after an earlier
physical collision and is not a singularity of the next-collision map.

### 2.3 Complete incidence tables

For every source chart the checker forms all unordered pairs and triples of
its candidate target list.  Every pair is classified as exactly one of:

- `empty`;
- `regular_noncoincident`, with the assembled double-radical coefficient
  envelope verified;
- `duplicate_cancelled`, with equal physical trace and equal coefficient
  proved before absolute values;
- `joint_normal_form`, with a separate integrability certificate.

Every triple receives an analogous explicit classification.  It is not valid
to omit a zero-dimensional incidence as “measure zero”: a critical germ or a
coincident inverse-square-root factor can make a difference quotient
nonintegrable.

### 2.4 DQ and matching layer

The event table is still not Gate 3 until all persistent cores and event rows
assemble into the global finite-DQ current, with boundary tightness and exact
restrictionwise scalar-current matching.  This must include source motion on
the white component as well as target motion; the angle derivative of
`Delta_k` alone does not compute the transfer-operator defect.

### 2.5 Current hard failures

The checked snapshot has a certified `tau_max<3`, an expanded 162-target lift
universe and eight source charts, but still has:

- no chart-specific candidate-target lists for any of the eight charts;
- zero instantiated event rows;
- zero pair/triple incidence rows;
- no first-hit partition, parameter-continuation, global DQ or scalar-match
  certificate.

These are missing data, not merely missing prose.  Gate 3 therefore remains
open even though the single-event critical-germ obstruction has been removed
for every already selected forward circle target.

## 3. Gate 4: one incidence, two views, one charge

### 3.1 Required immutable record

For each physical incidence `a`, the base record is

\[
 (a,\operatorname{phys}(a),m_a,q_a,
  \operatorname{pol}(a),\operatorname{owner}(a)).
\]

It contains two **alternative**, nonadditive representations

\[
 J_a=\langle U_a^-\nu_a^-,E_a^-\rangle
    =\langle U_a^+\nu_a^+,E_a^+\rangle.
\]

Every base field is byte-for-byte equal in the two view records.  The only
fields allowed to differ are the oriented source/operator/test
factorization and its recovery clock.  Before `(m,n)` is known, define

\[
 q_a=\max\{C_a^-,C_a^+\}\,m_a.
\]

The `max` is charged once.  Neither `q_a^-+q_a^+` nor two separately selected
envelopes is the exact same-occurrence construction.

Each view must further carry:

1. the exact scalar-current identity on every record restriction;
2. a positive proper-family factorization after its recorded recovery time;
3. its recovery exponential moment under the same `q`;
4. all operator, carrier, boundary and density marks already absorbed into
   that `q`.

Only after this record is frozen may a deterministic policy select the
available long-side representation for a product-time query.  The unused
view is a representation, not an additional summand and not positive tail
mass.

### 3.2 Why the present two atoms are insufficient

The local v52 construction explicitly registers two extra indices
`i_ent` and `i_exit` and gives each its own coefficient/carrier/operator atom
and its own `q=C_core m`.  Those are valid local DQ atoms.  They do not prove
that either atom has the opposite representation, and they do not identify
the two coefficient measures as one physical incidence measure.

The following elementary no-go lemma makes the distinction strict.

**Separate-tag lemma.**  Let `a_-` and `a_+` be two additive positive
occurrences of fixed positive `q`-masses, with only reverse and forward
recovery respectively.  If both are active at query `(m,n)=(N,0)`, the
reverse-only occurrence has orientation-mismatch mass bounded below by its
fixed positive mass; hence it cannot satisfy `Ce^{-cN}`.  At `(0,N)` the
forward-only occurrence has the same defect.  Deleting the mismatched tag
after seeing `(m,n)` changes the immutable occurrence sum and violates exact
current/record matching unless that deleted scalar current is identically
zero.  Reinterpreting the two additive rows as two representations and
summing them instead counts the physical coefficient twice.

This lemma does not assert that a future global registry cannot reorganize
the local current.  It proves that the existing two-row evidence, by itself,
cannot discharge same-occurrence face time.  The missing object is precisely
one incidence row with two nonadditive views.

## 4. Literature audit and applicability

### 4.1 Stenlund's singularity result is qualitative, not the manifest

M. Stenlund, *A vector-valued almost sure invariance principle for Sinai
billiards with random scatterers*, arXiv:1210.0902, Section 4.1, defines

\[
 \mathcal S_c=F_c^{-1}(\partial M)
 \cup(F_c^*)^{-1}(\partial M^*\setminus\partial M)
\]

and states that it consists of piecewise smooth curves with a uniformly
bounded number of branches.  It also gives the primary/secondary
interpretation.  It does not give source-chart ids, lift ids, square-free
event equations, first-hit root comparisons, pair/triple resultants or
physical/source current coefficients.  It proves finiteness in principle,
not Certificate A.

### 4.2 Canestrari's 2026 discontinuous-map theorem is an exact template

G. Canestrari, *On linear response for discontinuous perturbations of smooth
endomorphisms*, Advances in Mathematics 497 (2026), 111008,
arXiv:2411.16628v3:

- Definition 2.2, (H1)–(H4), requires in (H4) a measurable foliation of the
  complement of the old/new discontinuity sets, a summable uniform
  correlation array `Theta_n`, and a separately scaled bound on the bad
  foliation part.
- Theorem 2.4 assumes the initial defect `nu_t/t` converges to a finite signed
  measure and then gives the response series.
- Proposition 2.5 decomposes that limiting defect into a Lipschitz density
  plus a finite singular measure supported on the unperturbed image
  singularity set.

This is the correct abstract shape for Gate 3 plus Gate 4: Gate 3 must produce
the finite initial singular current, while Gate 4 must propagate its exact
coefficient law through a uniformly summable foliation/recovery estimate.
The theorem does not construct either input for billiards.  The author
explicitly notes that verifying (H4) requires considerable work even for the
perturbed cat-map example.  Applying Theorem 2.4 without the global event and
same-`q` recovery records would simply assume the two gates being sought.

### 4.3 Latest small-hole billiard technology is only a partial recovery tool

*Linear response for Sinai billiards with small holes*,
arXiv:2604.19671v2 (2026), proves a small-hole response theorem.  In its source
notation, Lemma `push-vertical-line` turns the forward image of a vertical
line measure into a uniform standard family; Proposition
`invariance-standard-families` and Theorem `exp-mixing-sf` give invariance and
uniform exponential conditional mixing for regular standard families.

These results support the plausibility of recovery once a concrete source
curve has been produced.  They concern a fixed billiard map with a shrinking
hole, give a forward vertical-line construction, and do not identify the
moving-scatterer DQ current, its reverse representation, or a single exact
`q`.  They therefore do not close Gate 4.

## 5. Verifier contract and reproducibility

The verifier recomputes local provenance hashes and fails closed unless it
finds all of the following:

- numerical `tau_max` and its proof;
- nonempty source and target-lift universes with coverage proofs;
- one complete event row for every declared chart/target candidate;
- exhaustive pair and triple tables generated from that universe;
- global event coverage, first-hit partition, parameter continuation, DQ and
  scalar matching;
- one Gate-4 occurrence row for every Gate-3 occurrence id;
- forward and reverse nonadditive views with identical base fields;
- exact single-charge `max`-envelope digest;
- both proper-family and recovery-moment certificates;
- prequery orientation selection, orientation-tail, global exact-current and
  global exact-`q` certificates.

Run:

```bash
python3 -m py_compile deliverables/cm2_gates34_manifest_verifier.py
python3 deliverables/cm2_gates34_manifest_verifier.py --self-test
python3 deliverables/cm2_gates34_manifest_verifier.py \
  deliverables/cm2-gates34-event-q-manifest-2026-07-15.json
python3 deliverables/cm2_fixed_section_geometry_cert.py
python3 deliverables/cm2_standard_section_tangency_submersion_cert.py
python3 -m venv /tmp/cm2-flint-venv
/tmp/cm2-flint-venv/bin/python -m pip install 'python-flint==0.9.0'
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_standard_section_horizon_lift_cert.py
sha256sum -c deliverables/cm2-gates34-assault-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

Expected results:

- syntax compile: exit 0;
- verifier self-test: exit 0, `SELF_TEST: PASS`;
- actual evidence snapshot: exit 2, Gates 3 and 4 `NOT_CERTIFIED`;
- both existing geometry scripts: exit 0;
- horizon/lift certificate: exit 0, 35,024 leaves, maximum depth 14,
  `tau_max<3`, both lift families `[-4,4]^2`;
- frozen v52 manifest: every row `OK`.

## 6. Minimal next input that can change the decision

For Gate 3, the horizon, global target-lift universe and finite
disjoint-coverage source atlas now exist.  The next decision-changing artifact
is each source chart's certified candidate subset drawn from those 162 target
lifts.  Once those chart/candidate ids exist, the remaining event, incidence
and first-hit rows become finitely enumerable and the verifier will name every
missing tuple.

For Gate 4, the first decision-changing artifact is one positive-mass
physical incidence row whose forward and time-reversed coarea
parameterizations are proved to carry the same coefficient measure and exact
scalar current.  Define its single `q` by the maximum of both predictable
costs, then prove the two recovery moments without changing that record.  A
second separately weighted occurrence is not a substitute.

Until those artifacts exist, neither global DQ/matching nor same-occurrence
face-time may be promoted into an unconditional CM2 claim.
