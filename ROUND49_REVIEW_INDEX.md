# Round 49 — active review index

**Main article:** `ROUND49_REVISION.tex` — *Logarithmic-Depth Boundary Identification with Bounded Probes and Retained State*.

**Controlling report:** `REFEREE_REPORT_ROUND48_GPT6_PRO_HARSH.md` at `cd21a42e47faa8aee0979137da64bf77b016a201`.

**Point-by-point response:** `AUTHOR_RESPONSE_ROUND48.md`.

**Retained homogeneous results:** `ROUND49_RETAINED_RESULTS.tex`, using five unchanged Round 45 inputs. These are not dependencies of the new infinite-Jacobi depth result.

## Main mathematical entry points

| Requirement / advance | Source | Labels |
|---|---|---|
| Separate sampling and confidence-allocation weights | `round49/confidence.tex` | `thm:confidence`, `prop:visits` |
| Carry input-enclosure error and full-box witnesses | `round49/enclosures.tex` | `eq:representation`, `thm:outer` |
| Exact posterior at inverse-information cost | `round49/likelihood.tex` | `thm:variance`, `thm:posterior`, `cor:stage-rates` |
| Delayed short pulses to physical jets | `round49/sampled_generator.tex` | `lem:sampled-log`, `prop:block-certificate` |
| Same-law bounded-probe retained-state logarithmic depth | `round49/blocks.tex` | `lem:block-floor`, `thm:block-posterior` |
| Simultaneous delayed-pulse uncertainty | `round49/blocks.tex` | `prop:pulse-confidence` |
| All-policy information comparison | `round49/frontier.tex` | `thm:global` |
| Literature distinctions and main quantifiers | `round49/introduction.tex` | `thm:main` |

The attainable logarithmic bounded-probe result uses an explicit fast baseline gap and block-committed bounded profiles, with arbitrary feedback between blocks. Exploration still uses the original bounded-duration law and independent signs. Its exact posterior uses all completed blocks. It is not an arbitrary coarse-clock or arbitrary within-block-feedback guarantee. Leading constants and the full joint exponent curve are not claimed optimal.

## Reproduction

`ROUND49_PUBLICATION.json` records the genuine source-capsule commit, the full-history review-tree source commit, and their relationship. The source capsule contains the complete mathematical input/documentation closure; the full branch preserves all historical material. The GitHub tool blocked program-file writes, so the three validation/implementation programs are delivered in the accompanying `ROUND49_REVIEW_BUNDLE.tar.gz`, not committed as new `tools/` or `tests/` files. Their SHA256 hashes are fixed in `round49/SOURCE_MANIFEST.json`. Extract that bundle into a checkout of this revision without changing the mathematical inputs. With the indicated commit available:

```sh
SOURCE_SHA=$(python3 -c 'import json; print(json.load(open("ROUND49_PUBLICATION.json"))["source_capsule_commit"])')
python3 tools/verify_round49.py --source-sha "$SOURCE_SHA" --build
```

The verifier checks actual committed mathematical/documentation bytes and both active input graphs, separately verifies the supplied programs against the manifest-pinned SHA256 hashes, runs the tests, builds both documents three times in isolated directories, checks TeX recorder inputs, and rechecks all source bytes. A successful actual execution writes `ROUND49_VERIFICATION.json`, both PDFs, logs, and `ROUND49_REVIEW_BUNDLE.tar.gz`. The manifest does not hash itself recursively: its own bytes are bound by the source commit.

Tests alone:

```sh
python3 -m unittest discover -s tests -p test_round49.py -v
```

The tests include exact finite mathematics and software/source-integrity fixtures; they are not all-depth or proof-assistant certification. The publication receipt records actual execution, not merely intended commands. No successful remote runner is presumed.

## Exact computation

```python
import sys
from fractions import Fraction as F
sys.path.insert(0, "tools")
from round49_certificates import Box, grid_certificate
box = Box(F(1), F(2), F(1,2), F(1), F(3), F(4), F(1))
cert = grid_certificate(box, 2, F(1,16), mode="block", rho=F(1,2))
cert.validate()
print(cert.order)  # The direct certificate pays the whole successful-block probability.
```

`visit_budget` requires sampling and confidence-allocation arguments separately. `Band` requires an explicit representation-error budget. `outer_confidence` returns projected boxes, full witness boxes, and statistical/representation/tail/mesh/numerical components. Its `radius_budget_satisfied` method checks only the radius arithmetic; an identifying-grid hypothesis is still required for coefficient diameter. Resource caps raise an exception instead of returning an incomplete union.
