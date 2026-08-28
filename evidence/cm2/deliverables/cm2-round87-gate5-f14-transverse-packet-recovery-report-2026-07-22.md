# CM2 Round 87: weighted-BV packet disintegration and F14 integration frontier

## Frozen conclusion

The weighted transverse disintegration is certified on all 152 current
finite-root packets.  F14 itself is **not** certified, and candidate-local
maturity remains `13/18`.

In collision coordinates

\[
r=R\arcsin t,\qquad \phi=\arcsin p,\qquad v=\phi-4r,
\]

write

\[
h_v={\cos\phi\over\sqrt{17}},\qquad
m(v)=\int_{I_v}\cos(4r+v)\,dr,
\qquad M=(r_1-r_0)(p_1-p_0).
\]

The normalization is exactly

\[
d\Lambda(v)={m(v)\,dv\over M},\qquad
\rho_v={h_v\over m(v)},\qquad
\int d\Lambda=1,\quad \int_{W_v}\rho_v\,ds=1.
\]

The certified recipient is only

`X_BV = direct_sum_(152) L1(Lambda_i; BV_internal(W_i,v))`,

where `BV_internal` does not add zero-extension endpoint jumps, and
`S(c)_v=c rho_v`.  For every positive-mass fibre,

\[
m(v)\|\rho_v\|_{BV,\mathrm{internal}}
=\|h_v\|_{BV,\mathrm{internal}}.
\]

Thus the corner normalization singularity cancels in this precisely stated
space.  The synthesis cost is uniformly below `4300`.

## Exact integration audit

The certificate pins and crosswalks the Round85 operator frontier, Round25
packet registry, and Round27 F10/F13 registry.  Every output row carries:

- `candidate_packet_id`;
- `physical_homogeneity_subbranch_id`;
- `roof_level_j=0`;
- the immutable Round27 `F10_slot_id`;
- `immutable_F14_slot_id=NOT_MATERIALIZED`.

The exact census is:

- 152 Round25 packet-key crosswalks;
- 152 Round27 F10 slot crosswalks;
- 152 normalized weighted-BV disintegrations;
- 304 zero-mass support endpoints;
- 0 registered immutable F14 slots.

The accepted frozen strong source cost is

`M*(1+Reg_alpha(rho)+1/length)`.

The mass-weighted `1/length` (short-fibre/Z) contribution is uniformly below
`4300`.  What remains absent is a certified crosswalk from the internal-fibre
BV or coordinate log-Lipschitz control to the frozen dynamic
`Reg_alpha` mark, together with its recovered-strong intertwiner.  Moreover,
the Round27 F10 value is an empty physical-occurrence-face sum of zero; it
cannot be reused to pay this nonempty packet regularity term.

Therefore no immutable F14 slot is installed.  Candidate-local maturity stays
`13/18`, global Gate 5 stays `10/18`, and complete 18-field blocks stay zero.

## Verification

The producer uses 512-bit Arb arithmetic.  The 768-bit verifier independently
recomputes, rather than trusting status strings:

- all 152 interior-fibre positivity proofs;
- all 304 endpoint zero-mass identities;
- all 152 conditional-probability identities;
- all 152 transverse `Lambda` probability identities;
- all 152 internal-BV cancellations;
- all packet and F10 immutable-key crosswalks;
- the official zero registered-F14-slot ledger.

It rejects 7/7 semantic mutations, 14/14 pin mutations, and 4/4 strict-JSON
attacks.  Producer and verifier cold replay byte-for-byte against the frozen
JSON.

The next lawful promotion requires an immutable same-key F14 slot on the
accepted `M*(1+Reg_alpha+1/L)` completion plus a proved `Reg_alpha` recovery
intertwiner.  Weighted BV alone is not relabelled as that object.
