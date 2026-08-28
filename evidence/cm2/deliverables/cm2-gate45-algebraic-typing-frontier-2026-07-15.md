# CM2 Gates 4--5: global algebraic typing frontier

Date: 2026-07-15  
Model: centred rational two-disk pilot on the standard solid-boundary section
`N=G disjoint-union W`  
Verdict: **the global finite/Borel Kac algebra and scalar cancellation are
closed; physical Banach typing, stopped recovery and both CM2 norm lifts are
still `NOT_CERTIFIED`**

## 1. Independent replay

All commands used the pinned Flint/Arb environment:

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python ...
```

The following were independently replayed:

- the Gate-4 all-sheet certificate and verifier self-test: `exit 0`;
- the Gate-4 live completion check: expected `exit 2`;
- the global `Jx` reflection schema and verifier self-test: `exit 0`;
- its live Gates 4--5 completion check: expected `exit 2`;
- the Gate-5 prefix/suffix certificate and verifier self-test: `exit 0`;
- its live physical norm/phase check: expected `exit 2`;
- the corrected Gate-3 forward-time endpoint audit: the old 320 apparent
  descriptors and 16 apparent third-target vertices are retracted, with
  exactly zero physical transition vertices after correction;
- the positive-width component-local orbit
  `G(0,0)->tangent W(0,0)->G(1,1)`: `exit 0`;
- all three fixed SHA-256 manifests: every entry `OK`.

Thus this audit starts from the exact fail-closed frontier, not from a stale
positive snapshot.

## 2. Exact Gate-3/Gate-4 ledger identification

The executable integration check identifies the two independently built raw
universes as the same finite set, not merely sets of the same cardinality:

```text
Gate-3 global signed tangency sheets
  = Gate-4 merged raw signed sheets
  = 288.
```

They split exactly as

```text
128 parameter-active cross-colour sheets
+160 identically parameter-inactive same-colour sheets.
```

The active subset of the Gate-3 endpoint formulas is exactly the Gate-4 raw
active endpoint ledger:

| descriptor class | exact count |
|---|---:|
| target--target common tangents | 36,352 |
| source grazing | 256 |
| parameter-window boundaries | 256 |
| constant-polarity splits | 128 |

The all-sheet `Jx/Jy` universe has 72 four-element orbits; its active subset
has 32 four-element orbits.  This proves that the Gate-4 schema is neither
missing nor double-counting a parameter-active raw sheet.

This remains a raw analytic ledger.  A raw sheet or endpoint descriptor is
not an immutable connected physical occurrence row.

The corrected forward-time audit is now binding provenance.  The former
pre-audit list contained 320 apparent descriptors and generated 16 apparent
third-target vertices.  Every such contact fails the missing forward-time
test (`ell_other<0`).  The corrected exhaustive interval audit has

```text
physical transition vertices                 0
physical transition-vertex Jx/Jy orbits       0
nonphysical tau=3 crossing collars            4
numerically unresolved collars                0.
```

Thus **zero** raw endpoint descriptors are promoted to physical event rows.
The only physical event input used below is the separately certified
positive-width component-local incidence
`G(0,0)->tangent W(0,0)->G(1,1)`.  It validates the same-occurrence schema on
one local orbit; it does not repopulate the corrected global registry.

## 3. Strongest unconditional algebraic conclusion

In the fixed collision-flux gauge the mean roof is constant.  Hence, whenever
the displayed Borel current pairings exist,

\[
 \mu_N(\dot r)=0.
\]

The complete `Jx` involution gives the same scalar identity rowwise in the
finite candidate schema: two-row orbits have opposite parameter polarity and
equal absolute coarea; a fixed-label row is anti-invariant under its internal
coordinate involution.  Therefore

```text
GLOBAL_SCALAR_ROOF_MASS_CANCELLATION: CERTIFIED.
```

Combining this with the exact finite prefix/suffix and Kac adjoint identities
closes the four-term **algebraic/Borel** centering formula

\[
 \dot{\mathcal S}h+\mathcal S\dot h
 -\dot r\,\widehat\mu(h)-r\,\widehat\mu(\dot h).
\]

The companion certificate replays this formula over exact rationals and
checks that its base mean is exactly zero.  It also checks the existing exact
endpoint adjoint pairing, normalized Kac tower pairing and current
prefix/suffix pairing.

For a completed singular occurrence the two coordinates

```text
(moving-level dot(S)h, roof dot(r)*mu_hat(h))
```

carry the fixed structural mark `(+1,-1)`.  They share one coefficient
measure and therefore require one charge

\[
 q_e=\max(C_e^{\rm fw},C_e^{\rm rev},2)m_e,
\]

not one charge per coordinate.  For a constant observable this singular
combination vanishes rowwise.  This is an exact universal schema; instantiation
still requires the physical row fields and recovery hypotheses.

## 4. Exact obstruction to a stronger algebraic promotion

Scalar cancellation does not type or cancel the full singular current.  On a
two-point reflection orbit let

\[
 J_n=n(\delta_a-\delta_b),\qquad J(a)=b.
\]

Then for every `n`

\[
 \langle J_n,1\rangle=0,
\]

but the reflection-odd test `(1,-1)` gives `2n`, and
`||J_n||_{TV}=2n`.  The executable checks the exact scale family
`n=1,2,4,...,64`.  Consequently neither global scalar roof cancellation nor
the exact `Jx` isometry yields:

- cancellation against arbitrary physical tests;
- a uniform source-current norm;
- a uniform test-pullback norm; or
- a global CM2 norm intertwiner.

The independent height-one quadratic branch, finite-cut and abstract
height-two periodic phase countermodels are replayed as well.  The latter is
a counterexample to the implication “bounded height implies aperiodicity”; it
is not the actual pilot phase graph.  A separate physical audit now proves
that the actual `M,W` and `G,W` component spanning graphs contain weight-one
and weight-two cycles and hence have cycle gcd one.  This component result
still does not prove operator-valued `D(z)` invertibility.  Thus bounded
return depth and finite Borel algebra cannot fill the analytic gap.

## 5. Exact conditional completion theorem

If a future certificate supplies, on one immutable registry,

1. connected physical event rows with constant miss trace and polarity;
2. forward and reverse carrier typing and finite costs on every row;
3. a controlled stopped interval/cylinder algebra or the actual Gate-2 PPE;
4. all homogeneous prefix/suffix quantitative constants;

then the already certified algebra yields, without further counting:

- the same-occurrence two-view identity on every row;
- one `q=max(Cfw,Crev,2)m` charge per occurrence;
- the four-term centered Kac current with the shared `(+1,-1)` mark; and
- global scalar roof mass zero under `Jx`.

The current data do not supply hypotheses 1--4 globally.  In particular,
the scalar identity cannot be used to cancel norms of oppositely oriented
rows, and the fat-Cantor stopped-restriction obstruction remains active.

## 6. Final gate verdict

```text
GATE3/GATE4 RAW-SHEET ALIGNMENT: CERTIFIED
CORRECTED GATE3 PHYSICAL TRANSITION VERTICES = 0: CERTIFIED
COMPONENT-LOCAL GROUPED INCIDENCE BASELINE: CERTIFIED
GLOBAL SCALAR ROOF-MASS CANCELLATION: CERTIFIED
EXACT FOUR-TERM BOREL KAC ALGEBRA: CERTIFIED
PER-OCCURRENCE SHARED KAC-MARK SCHEMA: CERTIFIED
SCALAR-TO-CURRENT-NORM PROMOTION: FALSE

IMMUTABLE PHYSICAL EVENT ROWS: NOT_CERTIFIED
ALL-ROW PHYSICAL BANACH TYPING: NOT_CERTIFIED
GLOBAL STOPPED-PARENT RECOVERY: NOT_CERTIFIED
GLOBAL SINGLE-CHARGE q LEDGER: NOT_CERTIFIED
PHYSICAL FOUR-TERM KAC TYPING: NOT_CERTIFIED
PHASE CM2 NORM LIFTS: NOT_CERTIFIED
GATE 4: NOT_CERTIFIED
GATE 5: NOT_CERTIFIED
```

The distinction between the exact Borel algebra and its missing physical
Banach realization is essential; no unconditional CM2 claim follows from
this integration result.
