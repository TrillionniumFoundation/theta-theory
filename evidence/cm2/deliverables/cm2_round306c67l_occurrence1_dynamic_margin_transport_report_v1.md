# C67-L occurrence-1 dynamic face/seam margin transport

## Verdict

PASS as a deterministic, fail-closed, zero-credit capability candidate. This
round does not promote D02 and does not write runtime or canonical state.

The producer independently reconstructs collision 1 on every physical
endpoint occurrence of every C60 atom. It does not consume C57-L1 boolean
transport flags as conclusions and does not promote C36 seed-collar lower
bounds to global bounds.

## Frozen census

- Endpoint occurrences: 26,206 total; 22,229 pass the raw frozen-owner and
  outgoing-chart test; 22,207 pass every applicable named margin.
- Exact atoms: 13,103 total; 11,114 raw pass; 11,103 full named-margin pass.
- Corridor edges: 1,042 total; 498 raw pass; 491 full named-margin pass.
- Source seams: 16 total; 15 raw pass; 13 full named-margin pass.
- Corridor cells: 1,044 total; 394 have every incident edge full-pass and 554
  have at least one full-pass incident edge. Neither count is whole-corridor
  or D02 credit.

The raw edge census is exactly 498: the frozen first owner is `W[1,0]` and the
outgoing chart is strictly `W` on every atom and both endpoint occurrences.
The stricter full census is 491. Seven otherwise raw-pass edges remain
fail-closed because 22 endpoint occurrences lack a strict C24 all-core
exterior separation.

Endpoint blocker census:

- `OWNER_UNRESOLVED_MULTI_CANDIDATE`: 1,773
- outgoing chart `N` / unresolved / `S`: 612 / 646 / 668
- first-owner mismatches `G[1,0]`, `G[1,1]`, `G[2,0]`, `G[2,1]`:
  102 / 102 / 36 / 38
- `C24_ALL_CORE_EXTERIOR_MARGIN_UNRESOLVED`: 22

## Numeric contract

Each endpoint interval directly recomputes the 55 retained candidates,
strict first-root order, frozen owner, outgoing chart, official `X+` wall
word and endpoint/crossing margins, H0 lower margin, incidence-rank-14
margin, and C24 all-core exterior margin. The other 106 radius-4 candidates
are bound by exact chart-global horizon or outgoing-halfspace exclusions.

Rational boundaries remain exact. Source seams use the pinned outward
isolating intervals `[707/1000,708/1000]` and
`[-708/1000,-707/1000]`, validated against the exact root of
`2*x^2-1`; both chart representations are recomputed and tied to the same
physical seam row. No point sampling, local-chart shortcut, or arbitrary seam
map is used.

## Independent verification

The independent verifier treats the producer source as opaque bytes and does
not import, decode, compile, or execute it. It reconstructs all 26,206 numeric
decisions and the atom, edge, seam, and corridor projections from frozen
upstream bytes. The verifier returns PASS with verification object
`fd8b0ce7d5414367e4107b018bed009bddb0574c3422abc635b853fb7f7b1dcf`.

All 12 coherent/file attacks fail closed, including owner, outgoing-chart,
credit, seam-polynomial, row-closure, aggregate-census, symlink, and hard-link
mutations. Inputs are opened with `O_NOFOLLOW`, require one link, and are
re-read for TOCTOU stability. Two producer runs and two verifier runs are
byte-identical.

## Frozen identities

- Producer source:
  `2b84ec3bb6e50d1ec5b1166cab7a2f66406739d3808e93a51b1ac9d536d90b24`
- Result file:
  `5b43ecb647958185859e987e5985660c660fb6a5ee7e422ae2748f96a880b8ac`
- Result object:
  `0e5b88cd4978661fdfad6bc508029f714e78a760f7164f4114cf540334b73fe1`
- Independent verifier:
  `8014b32ce466acf067972f2861527a37343a4b89bd7263dd8b486bd27b93e1da`
- Independent verification file:
  `0b8648f6bae78c7f0b632c762173d76de47fc3b3da034402bf10e22d6c825669`

## Strict boundary

Formal, D02, and handoff credit are all zero. No C67 file is an installed
authority. The 491 pass edges are a partial margin capability only; failed
atoms and edges remain explicit blockers. CM2 remains `NO-GO_FOR_CLAIM`.
