# CM2 Round 52 Gate-4 defect threshold and same-ID return frontier

Date: 2026-07-20  
Strict status: **the common terminal-survivor mass and the zero-shell parent transfer are now certified; the physical defect moment and common-intersection boundary geometry remain open. Gate 4 is not certified and CM2 remains NO-GO.**

## 1. Scope and append-only provenance

This leaf joins the Round-52 uniform C24 outer majorant to the Round-51
once-charged two-proper-view law, audits the proposed cell-level reindexing,
and sharpens the exact endpoint-tail rate needed for the remaining defect
moment.  No older artifact is modified.

The executable artifacts are:

- `cm2_gate34_round52_defect_threshold_same_id_return_frontier_cert.py`;
- `cm2_gate34_round52_defect_threshold_same_id_return_frontier_verifier.py`;
- `cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json`;
- `cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.sha256`.

The leaf pins the Round-35 same-ID carrier, Round-48 survivor kernel,
Round-50 physical grouping, both relevant Round-51 leaves, and the new
Round-52 outer-majorant manifest by exact SHA-256.

## 2. Uniform common terminal survivor: a real Gate-4 increment

The Round-52 numeric leaf constructs a parameter-independent Lipschitz
majorant

\[
  1_{C24}\le g_{\rm out}\le 1
\]

as the maximum of 24 trapezoid products.  Its exact certified bounds are

\[
  \mu_s(\operatorname{supp}g_{\rm out})
  <\frac{87603}{125000000}<\frac1{1000},
  \qquad
  \|g_{\rm out}\|_\infty+\operatorname{Lip}_1(g_{\rm out})<7251.
\]

Choose a single finite `H_joint` beyond the two uniform SYZ thresholds for
the Round-51 inner bump and this outer majorant.  It is uniform over
`|s|<=1/400` and over every normalized canonical proper input view, although
it is not numerical.  At the terminal collision,

\[
 \frac{21}{111718750}
 < \frac{h_{\sigma,\rm hit}}{p}
 < \frac1{500},
 \qquad \sigma\in\{\mathrm{fw},\mathrm{rev}\}.
\]

Consequently each marginal terminal survivor has mass strictly greater than
`499p/500`.  Pulling both predicates back to the same Round-51 raw physical
point and charging that parent once gives the exact union-bound conclusion

\[
  h_{\rm fw\cap rev}
  >\left(1-\frac1{500}-\frac1{500}\right)p
  =\frac{249}{250}p.
\]

This is only a terminal nonhit statement.  It does not say that either orbit
avoids C24 at intermediate collisions.

## 3. The old marginal-shell obstruction is eliminated

Round 48 defines the dyadic shell by

\[
  2^{-(k_\sigma+1)}p<h_\sigma\le2^{-k_\sigma}p.
\]

Here `h_sigma` is the survivor of this one common **terminal-cut schedule**;
it is not an all-intermediate-time avoidance mass.

Since `h_sigma/p>499/500>1/2`, both shells are identically zero:

\[
  k_{\rm fw}=k_{\rm rev}=0.
\]

The two postproperisation clocks therefore synchronize exactly:

\[
 C_{\rm fw,post}=C_{\rm rev,post}=H_{\rm joint}+221328.
\]

Moreover

\[
 p<\frac{500}{499}h_\sigma.
\]

Thus the survivor-supported Round-51 ambient two-view exponential-clock
estimate now transfers back to the parent charge.  The former abstract model with
`h_rev/p=2^-n` is incompatible with the new physical lower bound and is not
an active Round-52 obstruction.

The parent-charged postclock **ambient max-clock envelope** therefore has a
qualitatively finite `L^(6/5)` moment.  For the corresponding total ambient
envelope,

\[
 C_{\sigma,\rm total}
 =696\,\overline D+H_{\rm joint}+221328,
\]

the only variable obstruction is the same-kernel defect moment

\[
 I_D=\int p(y)e^{\overline D(y)/6}\,d\lambda(y).
\]

If `I_D<infinity`, the total ambient exponential envelope is integrable.
This controls its `L^(6/5)` envelope, and its absolutely continuous mass
outside any increasing full-mass Borel exhaustion tends to zero.

This does **not** type the envelope as the physical first-return charge `q`.
That promotion still requires a common-refinement boundary-`Z` estimate, a
proper same-ID common return, and the moment of every additional recovery
clock on that physical carrier.  Likewise, uniform integrability of an
absolutely continuous ambient envelope is not the strong singular/current
cemetery theorem.  The old marginal-shell obstruction is eliminated, but
physical `q`, its numerical value, and strong cemetery remain unclosed.

## 4. Exact defect-tail threshold

Round 51 gives

\[
 \overline D(M)=0\quad(0\le M\le310),\qquad
 \overline D(M)=M-309\quad(M\ge311).
\]

Put `a=exp(1/6)` and `T_m=nu{M>m}` for
`nu(dy)=p(y)dlambda(y)`.  The exact layer-cake identity is

\[
 I_D=\nu(X)+(a^2-1)T_{310}
 +(a-1)\sum_{m\ge311}a^{m-309}T_m.
\]

Therefore a pure exponential bound `T_m<=C b^m` is sufficient exactly on the
strict side

\[
 b<e^{-1/6}.
\]

In dyadic notation the critical exponent is

\[
 \alpha_c=\frac1{6\log2}=0.2404491734814939\ldots .
\]

The leaf proves the rational bracket

\[
 \frac76<e^{1/6}<\frac{241}{204}<\frac{13}{11}
\]

and hence the substantially weaker rational sufficient interface

\[
 T_m\le C_{1/4}\,2^{-\lfloor m/4\rfloor}.
\]

Since `(13/11)^4/2=28561/29282<1`, exact summation gives

\[
 I_D\le\nu(X)
 +\frac{11723}{54477219746384227185197056}\,C_{1/4}.
\]

This quarter-block rate is sufficient but is not yet proved for the physical
arbitrary-`R_n` law.

Sharpness is also explicit.  With `a=e^(1/6)`, atoms

\[
 M_k=311+k,\qquad w_k=(1-a^{-1})a^{-k}
\]

have exactly the critical tail, while every term
`w_k a^Dbar(M_k)` is the same positive constant.  Thus `I_D=infinity` at
equality.  A fully rational replay uses
`w_k=(1/7)(6/7)^k`; the lower bound `e^(1/6)>7/6` makes every moment term
strictly greater than `7/36`.

## 5. Cell-level reindexing: valid, useful, but not sufficient

Retaining `natural-short-cell-k` and `image-recut-rank` in the Round-35
restriction ID is a valid Borel reindexing:

- the Round-50 fibres are finite;
- half-open ownership partitions the parent kernel modulo the frozen null
  boundary;
- forward and reverse remain two views of one charge;
- one measured standard pair is a singleton whole standard family, and its
  own closed `696*Dbar` evolution properises it.

This genuinely removes *group-min poisoning*: one tiny cell no longer assigns
its worst length rank to unrelated long cells in the former whole group.

It does not by itself prove `I_D`.  Separate the leaf-density bound
`p_j<=rho_j ell_j` from the physical D1 density `d_D1`.  The available Hölder
route requires an outer-base integral of `sum_j rho_j`; the physical D1
moment instead integrates `d_D1^(6/5)` against cell mass.  Those are different
measures and different marks.

The exact logical countermodel is:

- on a `b`-band of width `2^-n`, split a unit fibre into
  `N_n=2^(n^2)` half-open cells;
- each cell has length `2^(-n^2)` and leaf density `rho_j=1`;
- take the physical D1 density to be one fixed finite constant `d_D1=D0`
  (compatible with a fixed finite rank such as `B=14`);
- `N_n ell_n=1`, so the band mass is exactly `2^-n` and total mass is finite;
- the D1-type cell-mass moment is
  `D0^(6/5) sum_n 2^-n<infinity`;
- the outer counting-density term on band `n` is
  `2^-n 2^(n^2)` and diverges;
- for `n>=18`, the band contribution to `I_D` is

\[
 2^{-n}\exp\!\left(\frac{n^2-309}{6}\right),
\]

whose successive ratio is

\[
 \frac12\exp\!\left(\frac{2n+1}{6}\right)>1
\]

and tends to infinity.

This is a countermodel for inference from the currently installed fields, not
a claim that the billiard realizes those multiplicities.  The precise new
tail interface is a physical bound on the outer counting-density/cell packing,
or directly the quarter-block tail for cell length rank.

## 6. Why mass `>249/250` still does not certify a proper common return

The new lower bound removes the old zero-overlap and thin-mass issues.  It does
not control boundary fragmentation under the Round-51 map

\[
 \Theta_y=P_{\rm rev,y}\circ P_{\rm fw,y}^{-1},
\]

which is currently certified only as a Borel measure isomorphism.

An exact field-level separator satisfies all new marginal mass bounds.  Let
both ambient laws be Lebesgue probability on `[0,1)`, with

\[
 F=R=[0,999/1000)
\]

in their respective views.  Both terminal hits have mass `1/1000`, which lies
strictly between the certified inner and outer hit bounds.  For `k>=1`, partition
`[0,999/1000)` into blocks of length `(999/1000)2^-k`; in block `k`, retain an
interval `A_k` of length `(998/1000)2^-k` followed by a gap of length
`(1/1000)2^-k`.  Set

\[
 A=\left(\bigcup_{k\ge1}A_k\right)\cup[999/1000,1).
\]

A countable interval-by-interval translation is a Lebesgue-preserving Borel
isomorphism `Theta` with `Theta(A)=R`.  In the forward view the same-ID common
survivor is

\[
 F\cap\Theta^{-1}(R)=\bigcup_{k\ge1}A_k,
 \qquad
 m(F\cap\Theta^{-1}(R))=\frac{499}{500}>\frac{249}{250}.
\]

Nevertheless its canonical boundary numerator is

\[
 J=\sum_{k\ge1}\frac{m(A_k)}{|A_k|}
  =\sum_{k\ge1}1=\infty.
\]

This is not an artefact of choosing the displayed canonical representation.
A positive regular density has full support on its connected carrier `W`, so
the positive-length gap after each `A_k` prevents a carrier contained in the
survivor from joining two distinct `A_k`.  If `I_k` is the representation
fibre over `A_k`, then `|W_a|<=|A_k|` and

\[
 \int_{I_k}d\lambda=\mu(A_k)=|A_k|,
 \qquad
 \int_{I_k}|W_a|^{-1}d\lambda\ge1.
\]

Summing over `k` forces `J=infinity` for every positive regular
representation.

So large common Borel mass plus two marginal proper views does not, by itself,
give a proper common standard family.  This is not a physical counterexample;
it identifies the exact missing physical theorem: a curvewise regularity or
common-refinement estimate for `Theta` and the two terminal predicates that
makes the common boundary-`Z` numerator finite, together with the uniform or
moment control needed by closed properisation.

## 7. Corrected strict frontier

Certified in this leaf:

1. uniform same-ID common **terminal** survivor mass `>249/250`;
2. `k_fw=k_rev=0` and synchronized postproperisation clocks;
3. transfer from survivor-supported to a parent-charged postclock ambient
   max-envelope;
4. total ambient max-envelope and its absolutely continuous
   Borel-exhaustion tail conditional on `I_D`;
5. exact critical tail exponent and the rational quarter-block sufficient
   bridge;
6. valid cell-level once-charge retyping, with its precise multiplicity gap.

Still not certified:

1. the physical quarter-block/cell-packing tail and hence `I_D`;
2. a finite common-intersection boundary `Z` and a proper same-ID return;
3. physical first-return `q`, which additionally needs the proper common
   return and all recovery-clock moments;
4. numerical `H_joint`, hence numerical `C_fw,C_rev,q`;
5. the strong singular/current cemetery interfaces;
6. Gate 4 and CM2.

The next shortest route is therefore:

1. prove a physical cell-packing/counting-density estimate at any dyadic rate
   strictly faster than `2^(-m/(6 log 2))`; the rational target
   `2^(-floor(m/4))` is sufficient;
2. in parallel, put `Theta` and both terminal predicates into one curve metric
   and bound the common-refinement boundary numerator;
3. properise that positive common subkernel, install every additional
   recovery-clock moment on the same physical carrier, and only then construct
   `q` and its strong cemetery; the present `I_D` bridge controls only the
   ambient max-clock envelope;
4. separately numericalize the hidden SYZ scalars if a fully numerical clock
   is required.

## 8. Verification

The verifier independently recomputes the exponential bracket, layer-cake
coefficient, critical countermodel rows, outer-majorant inequalities,
cell-multiplicity rows, and large-common-mass separator.  It is fail-closed on
dependency hashes, exact schema, duplicate JSON keys, non-finite constants,
replay mismatch, and adversarial status promotion.  The final test counts and
hash ledger are recorded with the manifest.

Final replay results:

- Python syntax: `2/2 PASS`;
- dependency and exact-SHA validation: `8/8 PASS`;
- integrity, deterministic replay, and independent arithmetic: `PASS`;
- adversarial mutations: `101/101 REJECTED`;
- deterministic manifest re-emission: byte-identical `PASS`;
- certificate and verifier default fail-close mode: both exit exactly `2`;
- strict gate verdict: `0/5`, CM2 `NO-GO_FOR_CLAIM`.
