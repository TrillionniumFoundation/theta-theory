# Immutable inputs

| Role | Object |
|---|---|
| Canonical restart | `18000b21e4bfd89180ccb069e46ac0f21621f34d` |
| Complete R27 head | `c5f05d1944251a95619d5cdad814c5c83646429c` |
| R27 ordinary source | `4a9f9a36f6ad02561f8e8eae112674f3f3c5d777` |
| R27 native tree | `36c91366f880989e6e2836d7e7bf55e6666d4953` |
| R27 artifacts | `6ca75d078bc710cdbdf2feedf5744409947aaa37` |
| Latest R27 external report commit | `00cad841267ee714f20d71ca9734dc5d4014ee4f` |
| Exact external report blob | `79c032f1bd1697722d44206dfb28f48b1cdf2311` |
| R28 research-only intake | `37826ed38311e247874c35674e668855402ed6ff` |
| R29 canonical provenance merge | `d36133d6eab31b3c76a3e1e58d23fed8a9a7dd82` |
| R29 research contract | `c929b4b525b90afbf79e598d0f03a202aea6b243` |

The exact report is preserved as `review_inputs/R27_EXTERNAL_REFEREE_REPORT.md`, with its Git blob checked separately from the mathematical-source projection. The projection excludes review inputs and generated artifacts/evidence; publication additionally records the actual native directory Git tree, which includes the pinned review input. These two trees are not conflated.

The four canonical control files remain unchanged. All inherited paper subtrees and the R28 intake remain byte-identical Git objects. Old review, realization and frozen archive branches are never write targets.
