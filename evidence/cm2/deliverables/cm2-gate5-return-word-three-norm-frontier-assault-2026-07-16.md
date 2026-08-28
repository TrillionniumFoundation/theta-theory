# CM2 Gate 5: return-word registry and three-norm frontier assault

Date: 2026-07-16 (Asia/Shanghai)  
Model: centred rational two-disk torus pilot  
Frozen inputs: the first-hit target atlas, finite measurable prefix/suffix
ledger, corrected Kac ledger, actual phase graph, finite-`s` one-collision
recovery ledger, and tenth-round Gate-5 frontier were read only

## Verdict

Gate 5 remains **`NOT_CERTIFIED`**, but the vague phrase “finite return-word
registry” is now replaced by an exact executable frontier.

1. Every regular first return to the standard collision section lies in one
   of **441,280 immutable candidate word keys**.  The keys are frozen by the
   digest

   ```text
   841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9.
   ```

   Empty parameter fibres are allowed.  The exact set of nonempty keys is not
   claimed.
2. Every key has a symbolic prefix/suffix factorization at each roof level.
   There are **3,286,976** such level-factor pairs and **3,728,256** boundary
   split positions.
3. The physical homogeneous subbranch table and all 18 quantitative operator
   fields remain absent.  Consequently the regular-density,
   standard-family, flux/face and dynamic-test intertwiners, the full physical
   four-term Kac output, and operator Wiener phase transfer are still open.

This is the maximal executable registry sublayer supported by the frozen
geometry.  It is strictly stronger than a height-only existence argument and
strictly weaker than the required complete return-word **operator** registry.

## 1. What existed before this assault

The frozen evidence supplied four separate facts:

- `tau_max<3`, target lifts in `[-4,4]^2`, and return height at most nine;
- eight dominant source-normal charts and an exact classification of all
  `8*162=1296` chart-target pairs into 448 retained and 848 certified empty
  pairs;
- finite Borel prefix/suffix and Kac algebra with TV/`L^infinity` constants
  one and Kac height constant nine;
- three physical component edges proving standard-`N` cycle gcd one.

It did **not** contain a list of all physical nonempty return words, a
homogeneity partition for each word, or any word-indexed operator constant.
The earlier three phase edges are a spanning graph, not the return partition.

## 2. Exact crossing-word grammar

Between two solid collisions the lifted trajectory is a straight segment of
length less than three.  The conservative horizon argument allows at most
four recorded clean transparent-wall crossings in either coordinate.  On a
straight segment the sign in each coordinate is fixed.  For `n_x,n_y` in
`{0,...,4}`, choose the sign once when the corresponding count is nonzero and
shuffle the `n_x` horizontal-coordinate and `n_y` vertical-coordinate events.

Writing `sigma(0)=1` and `sigma(n)=2` for `n>0`, the exact number of crossing
patterns is

```text
sum_(0<=n_x,n_y<=4)
  binomial(n_x+n_y,n_x) sigma(n_x) sigma(n_y)
= 985.
```

The exact wall-count histogram is

| wall records | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| patterns | 1 | 4 | 12 | 28 | 60 | 120 | 200 | 280 | 280 |

The event alphabet is `X-`, `X+`, `Y-`, `Y+`.  Simultaneous corner crossings,
grazing hits and source-chart seams are assigned to the singular
cemetery/one-sided-trace interface; they are not silently treated as regular
operator rows.

## 3. Immutable candidate key registry

A key is

```text
(source normal chart, retained target lift, monotone clean-wall record).
```

The source chart is one of

```text
G:E, G:W, G:N, G:S, W:E, W:W, W:N, W:S.
```

The target is one of the exact retained pairs from the frozen first-hit
classification.  The target universe has two obstacle labels and 81 lifts
per label.  For every fixed parameter `s`, the associated Borel fibre is

```text
D_w(s) = {x in the source chart:
          the ordered clean-wall records equal w and
          the next solid first hit is the recorded target}.
```

Empty fibres remain in the common key universe.  Thus

```text
448 retained chart-target pairs * 985 crossing patterns
= 441280 candidate keys.
```

The roof histogram is:

| roof | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| keys | 448 | 1792 | 5376 | 12544 | 26880 | 53760 | 89600 | 125440 | 125440 |

The chart-target digest is

```text
ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75,
```

and the 985-pattern digest is

```text
2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d.
```

Every regular physical first return has one key after the declared seam
convention.  Hence this is a collision-SRB full-measure **key envelope**: the
usual grazing/corner singular set has zero collision-flux measure.  It is not
an exact list of nonempty domains and not a physical operator table.

## 4. Prefix/suffix namespace

For a word `w` of roof `r(w)` and `0<=j<r(w)`, the registry declares

```text
P[w,j] = U_c^j restricted to D_w,
S[w,j] = U_c^(r(w)-j) on U_c^j D_w,
<S J P nu,phi> = <J P nu,S^* phi>.
```

Summing the roof histogram gives exactly

```text
sum_w r(w)     = 3286976 level-factor pairs,
sum_w (r(w)+1) = 3728256 endpoint boundary splits.
```

This is a complete symbolic Borel factorization.  The subbranch index `h` in
`(w,h,j)` is not materialized because no complete physical homogeneity table
exists.  Calling these formulas “homogeneous operator blocks” would therefore
be an overclaim.

## 5. The 18 missing physical operator fields

For every `(word key, homogeneous subbranch, roof level)`, the immutable
schema requires:

1. nonempty-or-empty domain proof;
2. physical homogeneity subbranch table;
3. homogeneous prefix chart;
4. homogeneous suffix chart;
5. inverse-Jacobian bound;
6. log-Jacobian distortion sum;
7. one-step cut-growth/`Z` sum;
8. face transversality lower bound;
9. face `C2` atlas bound;
10. coarea-density regularity bound;
11. dynamic-Hölder test pullback;
12. `C1` face-trace pullback;
13. moving-boundary DQ current and both traces;
14. regular-density operator cost;
15. standard-family operator cost;
16. flux-face operator cost;
17. dynamic-test operator cost;
18. operator phase block.

Their schema digest is

```text
bc7f3bfd5ff896e5de853cfa6f96327ec21fb983359becb40da9526be98c51a5.
```

The first undecided field is domain nonemptiness.  The first strong-norm
field is the homogeneity partition.  No complete physical operator block is
currently populated.

The existing constants remain valid seeds:

```text
Borel TV/L-infinity prefix/suffix       1,
Kac height                              9,
one-collision geometric seed            204*2^B_s,
one-time standard-family boundary       C_mesh*2^K,
C_mesh                                  69986663973833932800.
```

They are occurrence-level or weak-norm statements.  They have not been bound
to every word key and are not copied into the missing fields.

## 6. Why the three CM2 intertwiners still do not follow

Three exact countermodels keep the boundary sharp.

### 6.1 Regular density and dynamic tests

The single height-one word `H(x)=x^2` has deterministic pushforward TV norm
one.  At `y=1/n^2`, both the pushed density and inverse speed are `n/2`; the
replay reaches 64.  Thus one Borel word and constant one do not bound density
variation or inverse `C1` test pullback.

### 6.2 Standard-family and flux/face cutting

Split one unit-mass curve into 64 pieces of length and mass `1/64`.  TV stays
one, but the positive-decomposition curve cost rises from 2 to 65, an exact
factor `65/2`.  A finite word key therefore does not control `Z`, face cuts,
or atlas multiplicity.

### 6.3 Component gcd versus operator phase

A one-component, weight-one graph has cycle gcd one.  On a hidden fibre let
`U=diag(1,-1)`.  The centered vector in the second coordinate makes
`I-zU` singular at `z=-1`.  Hence component gcd one removes the elementary
period obstruction but does not prove operator Wiener invertibility.

## 7. Kac and phase boundary

The following remain certified:

```text
finite-Borel four-term Kac algebra                  exact,
singular event-current TV                           <=16128/5,
height-nine singular phase-lift envelope             <=290304/5,
standard-N component cycle gcd                       1.
```

The two regular Kac terms are not separately typed in CM2 spaces, and the
singular terms are not propagated through all return words in those spaces.
Therefore the full four-term physical Kac output is not certified.

The preferred `direct_standard_N` route introduces no separate phase tower.
For the optional fixed-to-full route, the absence of word-indexed operator
blocks still prevents an operator Wiener theorem.

## 8. Gate 2 nonpromotion audit

This registry lives on the collision section `N=G disjoint-union W`.  It
covers the regular collision-SRB domain modulo its standard singular set, but
it is **not** a stable-saturated Young base.  In particular it supplies none
of:

- a stable holonomy quotient or quotient density `rho`;
- onto inverse branches and physical reverse weights;
- the one-state full-branch quotient;
- a native stopping antichain or endpoint typing.

The independent Gate-2 audit still has at least `0.903` of the candidate
common rectangle unregistered.  Therefore the 441,280 Borel keys do not feed
the Gate-2 one-state quotient and do not change Gate 2's status.

## 9. Latest technology audit

A direct arXiv API query on 2026-07-16 for dispersing/Sinai billiards and
return/transfer operators found no newer theorem that fills the word-indexed
fields above.  The closest current sources remain:

- Demers--Liverani, arXiv:2606.10155v1: regular-density anisotropic spaces and
  a review of sequential billiards, but no characteristic-function-stable
  wordwise restriction theorem for these moving faces;
- Canestrari, arXiv:2604.19671v2: linear response for a fixed Sinai billiard
  with a shrinking boundary hole, not moving-collision return blocks;
- Climenhaga--Day, arXiv:2604.25881v1: a symbolic construction of the unique
  measure of maximal entropy, not the collision-SRB strong-norm
  prefix/suffix/Kac interface.

Thus no cited result turns the finite key envelope into the missing
homogeneous physical operator table.

## 10. Exact remaining Gate-5 boundary

```text
REGULAR RETURN-WORD CANDIDATE KEY ENVELOPE:       CERTIFIED
IMMUTABLE 441280-KEY DIGEST:                      CERTIFIED
SYMBOLIC PREFIX/SUFFIX AT ALL 3286976 LEVELS:     CERTIFIED
PHYSICAL BOREL TV/Linf CONSTANTS:                 CERTIFIED

EXACT NONEMPTY WORD-DOMAIN DECISIONS:             NOT CERTIFIED
PHYSICAL HOMOGENEITY SUBBRANCH REGISTRY:          NOT CERTIFIED
COMPLETE RETURN-WORD OPERATOR REGISTRY:           NOT CERTIFIED
REGULAR-DENSITY PREFIX/SUFFIX INTERTWINER:         NOT CERTIFIED
STANDARD-FAMILY CM2 NORM LIFT:                    NOT CERTIFIED
FLUX-FACE CM2 NORM LIFT:                          NOT CERTIFIED
DYNAMIC-TEST CM2 NORM LIFT:                       NOT CERTIFIED
FULL FOUR-TERM PHYSICAL KAC CM2 OUTPUT:            NOT CERTIFIED
OPERATOR WIENER PHASE TRANSFER:                    NOT CERTIFIED
GATE 5:                                           NOT CERTIFIED
```

## 11. Reproduction

Use the frozen `python-flint==0.9.0` environment because the imported
first-hit classifier imports Arb:

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate5_return_word_three_norm_frontier_cert.py \
  deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py

$PY deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py \
  --replay --integrity-only
$PY deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py \
  --self-test

# Expected exit 2: physical homogeneous blocks and all strong lifts remain open.
$PY deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.sha256
```

The replay/integrity mode exits zero.  Nine independent mutations are
rejected.  Live mode exits two by design.
