# CM2 moving-billiard nonvacuity roadmap

Literature cutoff: 14 July 2026. This note separates proved technology,
new sufficient reductions established in the accompanying v46 manuscript,
and geometric statements that still have to be proved. It does not claim an
unconditional CM2 theorem.

## Executive decision

Keep two models, with different jobs.

1. **Deterministic final target:** a finite-horizon toral Lorentz gas in
   which one analytic strictly convex scatterer is translated by `s v`, with
   every shape and perimeter fixed. This is a genuinely non-conjugate moving
   path, while the collision space and
   `dμ = const · cos(φ) dr dφ` are exactly common to all `s`.
2. **First nonvacuity testbed:** Stenlund's fixed-section refreshed-scatterer
   model, with one fixed reference scatterer and one fixed-shape translated
   scatterer whose centre is refreshed on a compact admissible set. Use an
   iid `C¹` density bounded above and below. The fixed section preserves a
   common phase space, common collision probability, invertibility, and time
   reversal. This is the cleanest place to verify all bookkeeping and
   recovery interfaces before attempting a deterministic pathwise upgrade.

An explicit pilot inside Stenlund's construction is the fixed-grey /
translated-white two-disk model with radii `0.36` and `0.16` and centre
motion restricted to `ε = 0.005`. Its strict no-overlap, finite-horizon, and
free-zone margins make `c(s)=s v` a concrete nontrivial relative-translation
subclass on which finite clean cylinders can be certified before treating a
general analytic scatterer.

The refreshed model is not a substitute for the autonomous pathwise result.
It is an annealed/quenched proof laboratory in which the base change of law
can be made exactly diagonal.

## What v46 newly reduces

The latest manuscript makes two reductions that should be used in either
model.

- **Diagonal matching.** Construct the complete physical tree, source
  occurrence, signed current `m`, and positive envelope `q` on one unselected
  law. If the source carrier is the exact record-preserving pushforward of the
  physical carrier, all tree and carrier Radon–Nikodym ratios are one. The
  sole selection likelihood is then the total source envelope
  `q_η(Y_src)`. The proposal is also defined on zero-source parents by one
  fixed harmless probability.
- **One common complexity-moment criterion, instantiated on three laws.** After an
  accessible positive coarea component has entered a measured unstable
  family, set
  `𝔃 = 1 + (scaled density mark) + Z(family)`. If
  `R_rec ≤ C + C_rec log 𝔃`, a propagated global `q`-weighted power moment of
  `𝔃`, together with the same moment under the normalized shallow and deep
  laws, gives:

  - an absolute face recovery tail with every
    `c_R < χ_Z / C_rec`;
  - `SHREC(q_sh)` for
    `c_cpl^sh < q_sh < χ_Z / C_rec`;
  - `NREC_deep(q_deep)` for
    `max(α₊,α₋) < q_deep < χ_Z / C_rec`.

This closes the recovery algebra, not the geometric entry of an arbitrary
moving coarea face into an unstable family.

## Interface-by-interface route

| Interface | Literature-backed part | New lemma still required on the same descendants |
|---|---|---|
| face-time | SYZ Lemmas 13 and 16 give uniform density/boundary recursions; their Theorems 1′–2′ give uniform coupling after properness. Canestrari 2026 gives an exact vertical-source prototype. | Moving swept-face → positive measured unstable family, with exact motion/coarea density, Borel orientation, uniform `𝔃` moment, and an exponentially small no-orientation remainder. |
| PPE | Leclerc v2 and LPS v3 give quantitative Fourier/escape tools on hyperbolic or `C^{1+α}` quotient systems. | Transfer a terminal rough gate to the actual collision-SRB stopped descendant, prove the finite-holonomy derivative/sublevel estimate uniformly over every admissible polynomial, then verify PPE2–PPE4 on the identical labels. |
| change of law | A fixed collision section gives a common `M` and exact common `μ`; choosing the physical iid environment law as proposal makes its base RN equal to one. | Build one datum-independent incidence kernel before all selectors. If another environment reference is used, charge its entire block likelihood. |
| physical/source matching | The common-law diagonal realization removes artificial tree/carrier ratios. Stable-holonomy densities are uniformly controlled in SYZ. | Prove the record-preserving exact coarea pushforward simultaneously for signed `m` and dominating `q`, including the actual active slope-event inclusion. |
| shallow/deep | Growth lemmas give short-curve mass and logarithmic recovery; normalized `Z` moments give exponential recovery moments. | Either define the deep rank canonically by `ceil(|log |W||)` or prove a uniform inclusion between the manuscript's word depth and curve-length/recovery rank. Preserve both main and nonmain deep owners. |

## Fixed-section likelihood budget

Let the refreshed centre have density `p` on a compact admissible region
`B`, with `0 < p₋ ≤ p ≤ p₊`.

- If the proposal is the exact iid environment law and the source occurrence
  is its exact physical coarea pushforward, the base RN is one.
- Relative to uniform `u = 1/|B|`, an `N`-block density is bounded by
  `(|B| p₊)^N`, and the reverse density by `(|B| p₋)^{-N}`. If only one
  refreshed coordinate is active, only one such factor is paid.
- For a differentiable family `p_s` with
  `||∂_s log p_s||∞ ≤ L_p`, the `N`-block perturbative cost is at most
  `exp(N L_p |s|)`. At `N ≍ log(1/|s|)` this is `1 + o(1)`.
- Conditioning on survival through a hole of size `t` costs at most
  `(1-Ct)^{-n}` when the corresponding survival lower bound applies. For
  `n ≍ log(1/t)`, its logarithm is `O(t log(1/t))`, hence subexponential.

None of these estimates authorizes conditioning on a selected thin
descendant and then invoking ordinary memory loss. Selection stability must
be proved at the standard-family level.

## Concrete recovery budget

For a normalized unstable family with
`Z = Σ_j p_j / |W_j| ≤ B`,

`mass{|W| < ε} ≤ B ε`.

If growth gives `R ≤ χ |log |W|| + C`, then

`P(R > u) ≤ B′ exp(-u/χ)`

and every exponential recovery moment of order `< 1/χ` is finite. Splitting
at `R ≤ δN` gives the exact competing rates

- positive recovery tail: `δ/χ`;
- recovered signed core: `(1-δ)c_mix - a_fw`;
- orientation mismatch: `c_or`.

Thus the face-time exponent is

`min{δ/χ, c_or, (1-δ)c_mix-a_fw}`.

For deep words one must additionally prove the depth/length inclusion. If
deep rank is `ceil(|log |W||)`, the same `Z` estimate directly gives an
`e^{-L}` tail; the current manuscript's word depth cannot be silently
identified with that rank.

## Minimal lemma stack

The proof should be attempted in this order, with every lemma formulated on
the same master incidence space.

1. **Fixed-section geometry:** common `M`, exact common `μ`, time reversal,
   and uniform finite-horizon/hyperbolicity constants.
2. **Master incidence/coarea identity:** one projective Borel occurrence
   kernel, immutable records, exact signed current, and propagated positive
   envelope.
3. **Moving-face regularization:** constant-polarity patches; forward or
   reversed entry into a measured unstable family; exact density equal to
   the vertical-source prototype times the motion/coarea factor; uniform
   density and boundary-complexity moments; bad pieces assigned to the deep
   owner.
4. **Diagonal matching and likelihood:** proposal equals the physical
   occurrence law; `PROP_Q_MATCH`, event inclusion, and zero-parent
   convention; compute every non-unit likelihood explicitly.
5. **Integer recovery clock:** record `R_rec ∈ ℕ₀`; derive its global tail
   and normalized shallow/deep moments from the single `𝔃` moment in v46.
6. **Depth compatibility:** prove word-depth → short-curve/recovery-rank
   inclusion, or change the canonical record before any query.
7. **Terminal PPE gate:** hit a fixed rough terminal gate with exponential
   complement; propagate only the final `θN` segment; establish PPE1 on the
   actual SRB conditional and PPE2–PPE4 on exactly the same stopped labels.
8. **Rate closure:** insert the measured constants into the face, PPE,
   likelihood, shallow, and parameter-cutoff inequalities; choose
   `δ`, `θ`, `C_buf`, and `κ_L` only after all losses are charged.
9. **Quenched/pathwise upgrade:** replace an annealed exceptional-mass bound
   by a weighted Borel–Cantelli or a uniform pathwise statement. A union bound
   over symbolic words is not enough.

The first computer-assisted task should be deliberately finite: enumerate
the clean collision words reaching the fixed section and candidate magnet,
use interval arithmetic to certify the coarea Jacobian, orientation, and
native-coordinate terminal jet on each retained word, and send every failed
box to the already quantified deep owner. Such a calculation can certify the
finite rough gate; it cannot replace the analytic tails, projective-kernel
identity, or quenched upgrade.

## Terminal-gate PPE strategy

A full-depth jet bound is likely unnecessarily expensive. A better target is
a fixed finite rough gate followed by a short terminal propagation window.
Prove that the last `θN` block contains a certified gate, except on
collision-SRB mass `≤ C exp(-b θN)`. Conditioned on a hit, only `θN`
collisions contribute component proliferation, holonomy truncation, and jet
loss. Consequently every loss `aN` in the direct depth gate is replaced by
`aθN`, while the missed-gate exponent is `bθN`. One must then choose `θ>0`
small enough for the finite-type good-set window and large enough that the
missed-gate exponent survives every probability/likelihood loss.

Leclerc's roughness theorem can certify the fixed gate, but its equilibrium
measure on a hyperbolic/Cantor subsystem is not collision SRB. The gate-hitting
estimate must therefore come from the billiard's own standard-family or
Gibbs–Markov mixing, and the final sublevel estimate must be integrated
against the actual absolutely continuous unstable conditional.

The strongest existing gate-hitting template is the time-dependent coupling
magnet in SYZ §§5–7. After proper recovery, its first-coupled pieces form a
stopped antichain and Corollary 34 gives a geometric tail for the remaining
uncoupled mass, even though individual leftovers need not remain proper.
In SYZ block notation this gives
`b_gate = Δ⁻¹ |log(1-ζ̃/2)|`.
This can replace the stronger requirement that every miss-conditioned law
stay in one regular class. The still-new step is to put a uniform
all-polynomial rough certificate, in the original native coordinate, on the
magnet reference pieces.

## Current hard frontier

As of the literature cutoff, no cited theorem simultaneously supplies all
five interfaces for actual moving-billiard collision-SRB descendants. In
particular:

- the vertical-source calculation in Canestrari does not automatically
  cover an arbitrary moving swept face;
- sequential loss of memory does not imply stability after multiplying by a
  selected small-set indicator;
- Fourier decay on an Axiom-A or Cantor equilibrium state is not a polynomial
  small-ball theorem for collision SRB;
- generic analytic convex Birkhoff billiards are a different dynamical class
  from finite-horizon dispersing Lorentz gases;
- annealed refreshed-scatterer estimates do not imply the requested quenched
  pathwise CM2 conclusion.

The first genuinely decisive new result is therefore Lemma 3 above. Once it
is proved with the exact physical density and a power `𝔃` moment, v46 turns
face-time and both recovery interfaces into rate bookkeeping, while the
fixed-section construction turns change-of-law and physical/source matching
into a diagonal identity. PPE then becomes the only independent high-frequency
gate.

## Primary literature checked

- M. Stenlund, *A Vector-Valued Almost Sure Invariance Principle for Sinai
  Billiards with Random Scatterers*, CMP 325 (2014), 879–916,
  [arXiv:1210.0902](https://arxiv.org/abs/1210.0902),
  [DOI](https://doi.org/10.1007/s00220-013-1870-3).
- M. Stenlund, L.-S. Young, H.-K. Zhang, *Dispersing billiards with moving
  scatterers*, CMP 322 (2013), 909–955,
  [arXiv:1210.0011](https://arxiv.org/abs/1210.0011),
  [DOI](https://doi.org/10.1007/s00220-013-1746-6).
- M. Demers, H.-K. Zhang, *A Functional Analytic Approach to Perturbations
  of the Lorentz Gas*, CMP 324 (2013),
  [arXiv:1210.1261](https://arxiv.org/abs/1210.1261).
- M. Demers, F. Pène, H.-K. Zhang, *Local Limit Theorem for Randomly
  Deforming Billiards*, CMP 375 (2020),
  [arXiv:1902.06850](https://arxiv.org/abs/1902.06850).
- M. Demers, C. Liverani, *Projective Cones for Sequential Dispersing
  Billiards*, CMP 401 (2023),
  [arXiv:2104.06947](https://arxiv.org/abs/2104.06947).
- G. Canestrari, *Linear response for Sinai billiards with small holes*,
  v2 updated 21 May 2026,
  [arXiv:2604.19671v2](https://arxiv.org/abs/2604.19671v2).
- M. Demers, C. Liverani, *Recent Progress in the Application of Transfer
  Operators to Dispersing Billiards*, 8 June 2026,
  [arXiv:2606.10155](https://arxiv.org/abs/2606.10155). Problem 8.7 records
  the remaining small-set/aperiodic memory-loss obstruction.
- G. Leclerc, *Fourier decay of equilibrium states and the Fibonacci
  Hamiltonian*, v2 updated 1 July 2026,
  [arXiv:2507.23731v2](https://arxiv.org/abs/2507.23731v2).
- G. Leclerc, S. Paukkonen, T. Sahlsten, *Fourier decay in parabolic
  `C^{1+α}` systems with overlaps*, v3 updated 1 March 2026,
  [arXiv:2505.15468v3](https://arxiv.org/abs/2505.15468v3).
- I. Baldomá, A. Florio, M. Leguil, T. M.-Seara, *Chaoticity of generic
  analytic convex billiards*, 19 May 2026,
  [arXiv:2605.19897](https://arxiv.org/abs/2605.19897). This is a useful
  analytic perturbation clue, not a dispersing-billiard PPE theorem.
