# A2 revision 109 review entry

Branch: `revision/a2-v109-single-contact-multiplication-tomography-2026-09-21`.

Principal manuscript: `papers/A2-v17-boundary-information-coarsening/article/v109/paper.tex` — **Single-contact recovery of information metrics through polynomial multiplication**.

Complete retained companion: `papers/A2-v17-boundary-information-coarsening/article/v108/paper.tex`, including all four committed prepared inputs. No earlier mathematical source is deleted or overwritten.

Review response, dependency map, exact diagnostics, and build instructions are in `article/v109/RESPONSE_TO_R108.md`, `DEPENDENCIES.md`, `checks.py`, `verify.py`, and `README.md` under the paper root.

Controlling review commit: `5a8a8190e6a5979719591b286fca92aae3cc15cc`. Reviewed mathematical source: `4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191`. Preserved materialized companion inputs: `9affc52cc4eb62e5c14cffb564b380b86503aec2`.

The new theorem uses one contact point, not complete conormal data: for k=3d+2 it recovers 2k-1 native coordinates despite 5d(d+1)/2 unrestricted invisible directions. It includes necessarily noninjective full-symmetric measurements for d>=6. The principal article proves the product-space fibre criterion, native realization, stability, and a specified finite noisy contact-value experiment. Classical discriminant and generic statistical arguments are explicitly attributed.

The actual build receipt controls validation status. A queued workflow is not a success. `evidence/verification.json` denotes a source-bound Git build; `evidence/local-verification.json` denotes the explicitly distinguished local source-bundle replay. Source and generated evidence are separate commits.
