# Source-notation addendum

This supplements [REFEREE_REPORT.md](REFEREE_REPORT.md) and does not change its recommendation or the classification of its principal objections.

At the exact reviewed commit `c35b31b1924a1621374eab72ee60e4cb5ab37df5`, the decoded source of

`papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v24.tex`

shows the factor in `eq:v24-Lambda-R` as `ho(u,v)` following the equality sign, rather than the previously defined TeX factor `\rho(u,v)`. The intended formula, consistent with the density definition, the inherited endpoint-time theorem, and the new layer estimate, is

```tex
 d\Lambda_z^R=\rho(u,v)
  \mathbf 1_{\{y>U(u,v)z\}}\mathbf 1_{\{|y|\le R\}}\,du\,dv\,dy.
```

Restore the intended density token and inspect the corresponding typeset equation. This is a concrete source-notation correction, not a claim that the native build fails: bare letters can typeset without triggering a compilation error.

The positive assessment of the reverse-kernel construction in Section 2.3 of the report concerns this intended density formula. It is not an endorsement of a different, undefined intensity factor. This readily identifiable notation defect should not be inflated into a counterexample to the intended Poisson theorem.

No manuscript source was edited in this review branch. The correction is recorded here for the author to implement in a subsequent revision.

[Exact source](https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v24.tex)
