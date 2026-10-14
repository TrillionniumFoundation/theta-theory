# Build and verification protocol

Run `python seal.py` once before the ordinary source commit, after the exact R56 report is installed from its pinned repository blob. Then the source is immutable.

`python build.py --source-sha <40hex> --prepared-root <repository> --retained --output <outside-source-directory>` executes the native source/citation/label/recorder audit, normal and -O regression, two independent three-pass native LaTeX builds, then the complete retained R56 builder chain. No old publisher is executed. All binary artifacts, the prepared-source archive and build receipt are committed separately after source.

Independent rebuild starts from the actual downloaded remote prepared-source artifact, verifies every input binding, rebuilds outside its source tree, and checks unchanged inputs. Within-environment repeated PDF bytes must agree. Cross-environment bytes need not agree; compare normalized text, page counts and rendered pixels and report actual differences.

Builds and tests prove neither continuous mathematics nor priority. Source, binary and final read-only evidence SHAs are distinct and are recorded only after actual commits. The full-chain scope is the new native article and the complete R56 retained chain, not every historical paper in the repository.
