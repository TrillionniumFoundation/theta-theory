# Technical note: uniform high-frequency BDL bounds for the nonconjugate radial family

This note strengthens the exact-similarity witness by adding a nonconjugate family result at the level of **uniform estimates**, while keeping parameter derivatives separate.

Let `Q_a`, `a in I`, be the compact radial finite-horizon Sinai family from Paper I.  Shrink `I` so that the following strict geometric margins are uniform:

- lower and upper curvature bounds;
- lower free-flight and finite-horizon upper free-flight bounds;
- no multiple tangency in the selected finite flow-box atlas;
- uniform homogeneity-strip and complexity constants;
- uniform contact/temporal nonintegrability witnesses;
- uniform compact embeddings and Lasota--Yorke constants on the transported BDL spaces.

## Lemma 1 (finite-cover witness uniformization)

Suppose a fixed-table high-frequency proof is triggered by finitely many strict inequalities in a finite witness packet `W(a)`, and every entry of `W(a)` varies continuously inside one flow-box chamber.  If every `a in I` admits such a packet, then a finite cover of the compact interval supplies finitely many packets whose minimum strict margin is positive.  All constants produced by the fixed-table proof may therefore be chosen uniformly on `I`.

### Proof

Each strict packet is valid on an open parameter neighbourhood.  Choose a finite subcover.  Take the minimum of the finitely many positive margins and the maximum of the finitely many upper constants.  Every subsequent estimate is a finite monotone combination of these constants, so it is uniform.

## Theorem P2-BDL-HF-RADIAL-UNIFORM

For the compact nonconjugate radial family, the full fixed-table BDL high-frequency resolvent and exponential-mixing estimates hold with constants uniform in `a`.

The theorem concerns uniform bounds and resonance-free regions.  It does not claim that

\[
a\longmapsto(z-A_a)^{-1}
\]

is differentiable on one common high-frequency graph domain.  Such derivatives still require the complete graded generator-symbol packet.  The exact similarity theorem supplies an unconditional actual family where those derivatives are available.

## Combined Paper-II conclusion

```text
nonconjugate radial family: uniform full high-frequency BDL bounds
similarity family: uniform bounds + exact parameter derivatives
arbitrary nonconjugate family: graded symbol packet required for derivatives
```
