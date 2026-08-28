# CM2 Gate 3 fourth continuation: exact multiplicity normal forms and one event-row orbit

Date: 2026-07-15  
Scope: rational two-disk torus pilot, standard solid-boundary section
`N=G disjoint-union W`, complete eight-cell parent atlas and
`|s|<=1/400`.  The frozen v51/v52 files and the shared research log were not
edited.

## Decision

**All frozen pair/triple co-occurrence collars are now classified with
respect to physical simultaneous first occurrences, and one complete local
`Jx` event-row orbit is certified.  Gate 3 globally remains
`NOT_CERTIFIED`.**

The exact new conclusions are:

- every one of the `12,324` candidate pair rows in all eight charts has the
  normal form `distinct disjoint target circles`; equality of the two first
  roots is impossible;
- a line may be tangent to two distinct target circles, but the two contact
  times are rigorously different, so the two algebraic discriminants never
  represent two physical first events at one occurrence;
- consequently all `3,038` pair and `10,288` triple rows marked
  `unresolved_cooccurrence_collar` by the parent interval atlas contain zero
  simultaneous multiple first occurrences;
- exact `Jx/Jy` transport reduces those frozen registries to `1,519` pair
  and `5,144` triple representatives, with immutable mapping digests;
- the positive-width switching chart `G:E -> W[0,0]` and its reflected
  `G:W -> W[-1,0]` partner now have immutable local event rows with owner,
  hit/miss traces, polarity and coarea data;
- the eight true dominant-coordinate source seams have identical physical
  quotient traces and opposite artificial boundary orientations, so those
  duplicate chart faces cancel before absolute values.

This does **not** turn the 95,596 conservative `multi_candidate` boxes into
an exact global event partition.  It removes their multiple-first-event
obstruction; it does not determine the unique owner and single-target
tangency component at every point.  The global event table, DQ and
restrictionwise scalar matching remain fail-closed.

Evidence:

- `deliverables/cm2_gate3_normal_form_dedup_cert.py`;
- `deliverables/cm2-gate3-normal-form-dedup-manifest-2026-07-15.json`;
- `deliverables/cm2_gate3_normal_form_dedup_verifier.py`;
- `deliverables/cm2-gate3-normal-form-dedup-manifest-2026-07-15.sha256`.

## 1. Exact pair normal form

For a retained target lift `A`, write its center and radius as `a(s),R_A`.
The only possibilities are

\[
 G[i,j]=(i,j),\quad R_G=\frac9{25},
 \qquad
 W[k,l]=\left(k+\frac12+s,l+\frac12\right),
 \quad R_W=\frac4{25}.
\]

Distinct same-color lifts have center distance at least one.  For a gray and
white lift, the closest possible coordinate differences over
`|s|<=1/400` are `199/400` and `1/2`.  Hence

\[
 \inf_s |a(s)-b(s)|^2
 \ge \left(\frac{199}{400}\right)^2+\frac14
 =\frac{79601}{160000}.
\]

The largest cross-color radius sum is `13/25`, and therefore the uniform
squared separation margin is

\[
 \boxed{
 \inf_s\{|a-b|^2-(R_A+R_B)^2\}
 \ge\frac{79601-43264}{160000}
 =\frac{36337}{160000}>0.}
 \tag{1.1}
\]

The executable checks the sharper exact margin for every actual candidate
pair, rather than merely applying (1.1) as an unverified blanket bound.

### 1.1 First-root equality is empty

Suppose two incoming roots on the same source ray were equal to `tau`.
Then the single point `x=q+tau u` would satisfy both circle equations.
Subtracting them gives the exact linear radical-axis equation

\[
 2(b-a)\mathbin\cdot(q+\tau u)
 =|b|^2-|a|^2+R_A^2-R_B^2.             \tag{1.2}
\]

Substitution into either circle gives the circle-intersection resultant

\[
 -\{D^2-(R_A+R_B)^2\}
  \{D^2-(R_A-R_B)^2\},\qquad D=|b-a|. \tag{1.3}
\]

Both bracketed factors are positive under (1.1), so (1.3) is strictly
negative.  There is no common point and hence no equal first root.

### 1.2 A common tangent line is strictly time ordered

It would be false to say that two disjoint circles have no common tangent
line.  The needed physical statement is more precise.  If one oriented line
has signed transverse offsets

\[
 w_A=\epsilon_A R_A,\qquad
 w_B=\epsilon_B R_B,\qquad \epsilon_A,\epsilon_B\in\{-1,1\},
\]

then its two tangency times satisfy

\[
 (\tau_B-\tau_A)^2
 =D^2-(\epsilon_BR_B-\epsilon_AR_A)^2
 \ge D^2-(R_A+R_B)^2
 \ge\frac{36337}{160000}>0.             \tag{1.4}
\]

Thus the two contact times are strictly ordered.  If both are forward, only
the earlier can possibly be the physical first tangency; if a third target
comes earlier, neither later contact is a first event.  Algebraic
double-discriminant intersections therefore do not require a product-radical
normal form in the physical one-step current.

Every triple contains such a pair.  Hence no triple can be a simultaneous
first occurrence either.

## 2. What the 3,038/10,288 rows now mean

The parent atlas used `unresolved_cooccurrence_collar` only to say that two or
three labels survived interval pruning in one closed dyadic leaf.  It never
claimed a physical incidence.  The new theorem classifies every combination
in the larger candidate universe:

| universe | checked rows | physical simultaneous first occurrences |
|---|---:|---:|
| all candidate pairs | 12,324 | 0 |
| frozen unresolved pair collars | 3,038 | 0 |
| all candidate triples | 221,980 | 0 |
| frozen unresolved triple collars | 10,288 | 0 |

Per-chart ordered normal-form row digests are stored in the new manifest.
This is stronger than sampling the unresolved subset: every possible pair
and triple from the exact parent candidate lists is checked.

The statement is about multiplicity, not ownership.  A multi-candidate box
can still cross one target's tangency face, with one target first on the hit
side and another target first on the miss side.  That is a single physical
event face and still needs an event row.

## 3. Exact reflection deduplication

The parent certificate proved coefficientwise center-displacement identities
and candidate-list bijections for the only two reflections preserving the
horizontal displacement family.  The new executable transports every pair
and triple combination and verifies that its exact separation witness is
unchanged.

| representative -> partner | unresolved pair reps | unresolved triple reps |
|---|---:|---:|
| `G:E -> G:W` by `Jx` | 459 | 1,738 |
| `G:N -> G:S` by `Jy` | 459 | 1,740 |
| `W:E -> W:W` by `Jx` | 294 | 824 |
| `W:N -> W:S` by `Jy` | 307 | 842 |
| **total representatives** | **1,519** | **5,144** |

Every orbit has size two because the chart ID changes.  The totals double to
the frozen `3,038/10,288` counts.  For each orbit the manifest records:

1. the full combination-map digest;
2. the parent unresolved-row digest;
3. the representative counts;
4. the exact reflection axis.

No quarter-turn symmetry is used, since it leaves the horizontally displaced
parameter family when `s` is nonzero.

## 4. One immutable positive-width event-row orbit

The exact seed is

\[
 t=s=0,\qquad
 p_* =\frac{25\sqrt{610}-56}{674},\qquad
 \ell=\frac{\sqrt{610}}{50},
\]

and lies strictly inside `833/1000<p_*<834/1000`.

### 4.1 East row

On

\[
 |t|\le10^{-6},\quad |s|\le10^{-6},\quad
 \frac{833}{1000}\le p\le\frac{834}{1000},
\]

192-bit Arb proves one monotone physical first-tangency graph with:

- chart `G:E`;
- owner `W[0,0]`;
- hit side `p>p_*(t,s)`;
- hit trace: `W[0,0]` at target grazing coordinate `p_out=+1`;
- miss trace: the strict next target `G[1,1]`;
- miss-root minus tangency-time gap `>3/10`;
- `|partial_p Delta|>7/25` and `|partial_s Delta|>1/4`.

For this source/target color pair, at fixed `(t,p)`,

\[
 \partial_s\Delta=2wu_y,qquad
 \partial_p\Delta=\frac{2w\ell}{\sqrt{1-p^2}}.
\]

On the east row both are positive.  In the graph gauge the signed coarea
coefficient and graph velocity are

\[
 c_E=\frac{\partial_s\Delta}{|\partial_p\Delta|}
 =\frac{\sqrt{1-p^2}\,u_y}{\ell},
 \qquad
 \partial_sp_*=-\frac{\partial_s\Delta}{\partial_p\Delta}
 =-\frac{\sqrt{1-p^2}\,u_y}{\ell}.       \tag{4.1}
\]

The certificate proves `4/5<c_E<1` and `-1<partial_s p_*<-4/5`.

At the face, `w=R_W` and the target normal is `-u_perp`.  Specular reflection
fixes the tangent velocity, giving the declared hit trace.  With the owner
target removed, the interval root engine proves that `G[1,1]` precedes every
other retained target throughout the whole box, giving the declared miss
trace rather than an inferred sample label.

### 4.2 Reflected west row

Exact `Jx` gives

\[
 (t,p,s)\mapsto(t,-p,-s),qquad
 W[0,0]\mapsto W[-1,0],\qquad
 G[1,1]\mapsto G[-1,1].
\]

The partner box has `-834/1000<=p<=-833/1000`.  Direct Arb reevaluation, not
only symbolic copying, proves:

- chart `G:W`;
- owner `W[-1,0]`;
- hit side `p<p_*(t,s)`;
- hit trace grazing coordinate `p_out=-1`;
- miss trace target `G[-1,1]`;
- geometric `p` polarity `-1` and parameter-coarea polarity `-1`;
- the same absolute margins as the east row.

These two rows form one complete `Jx` symmetry orbit.  Their ordered schema
digest is

`e49696ec46c1f9f914ca7994ed7f57afb644bdda5cf1a71e22c8f256c011df17`.

They are genuine distinct-component traces on the solid-boundary section,
not a duplicate trace cancellation.  The global DQ polarity decomposition
is not inferred from these two local scalar coarea polarities.

## 5. Source-chart and lift seams

There are four dominant-coordinate seams on each source component:

`E/N`, `N/W`, `W/S`, and `S/E`.

On a seam the two formulas give exactly the same normal `n`, hence the same
`q`, tangent frame, `u`, discriminant, selected root and torus-valued target
trace.  Artificial chart-boundary orientations are opposite.  The eight
seam rows are therefore typed as
`duplicate_source_chart_seam_cancelled`, with null physical owner, and their
ordered digest is

`713e452d180e179850158a7f7c91e1ea2e83de50bd32dc864cefa4d358411036`.

Likewise, Euclidean lift representatives related by an integer translation
have the same torus-valued physical trace and cancel before absolute values.
Inside one fixed source lift, however, distinct target IDs are not called
duplicates: (1.1) proves that they are distinct circles and equal-time roots
are impossible.

The rational atlas padding beyond `|t|<=1/sqrt(2)` remains only a conservative
cover device.  Global assembly must restrict to the exact dominant-cell
assignment; padded overlap boxes do not create physical event rows.

## 6. Immutable event-row interface established here

Each closed local row contains the following immutable fields:

| field | content in this continuation |
|---|---|
| `chart_id`, `box` | exact rational source domain |
| `owner` | target lift whose discriminant vanishes first |
| `event_equation` | exact circle discriminant `Delta_T=0` |
| `root` | positive incoming tangency root `tau=ell` |
| `hit_side` | graph-side inequality in `p` |
| `geometric_p_polarity` | sign of `partial_p Delta` |
| `parameter_coarea_polarity` | sign of `partial_s Delta` |
| `p_coarea_coefficient` | `partial_s Delta/abs(partial_p Delta)` |
| `hit_trace` | target, contact formula, grazing output coordinate |
| `miss_trace` | exact next target, root and reflection formula |
| `certified_margins` | flight, root gap, submersion and coarea bounds |

This is an instantiated schema, not yet the global immutable event table.

## 7. Remaining finite registry and fail-closed layers

After this continuation, pair/triple **physical multiplicity** is no longer a
Gate-3 obstruction.  The finite residual registry is:

1. the 95,596 parent `multi_candidate` leaves, now known to contain only
   single-owner changes but not yet partitioned by their unique owner;
2. the four representative parent leaf registries `G:E`, `G:N`, `W:E`,
   `W:N`, with their frozen leaf and incidence digests;
3. all remaining connected single-target tangency components, including
   changes of the miss-trace target and endpoints at the true chart or
   grazing boundary;
4. source phase endpoints `p=+/-1` and any genuine return-chart endpoint
   typing;
5. the global regular/tangency current assembly, boundary tightness, owner
   partition and constant-polarity decomposition;
6. restrictionwise physical/source scalar-current matching.

Accordingly the new manifest marks the pair and triple physical
multiple-event fields certified, but leaves
`exact_resolution_of_multi_candidate_leaves`, `immutable_global_event_rows`,
`global_dq`, and `global_scalar_matching` null.  Gate 3 remains fail-closed.

## 8. Reproduction

```bash
python3 -m py_compile \
  deliverables/cm2_gate3_normal_form_dedup_cert.py \
  deliverables/cm2_gate3_normal_form_dedup_verifier.py

# Exact all-combination normal forms and direct Arb replay of the local orbit;
# about 12 seconds on the reference host.
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_normal_form_dedup_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_normal_form_dedup_verifier.py --self-test

# Optional replay of all new row digests and both local Arb rows.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_normal_form_dedup_verifier.py --replay

# Expected exit 2: the new normal forms pass, global event/DQ layers remain open.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_normal_form_dedup_verifier.py
```

The positive certificate exits `0`; verifier self-test exits `0`; the live
fail-closed verifier exits `2`.  The frozen v52 manifest is rechecked
separately and remains unchanged.
