# History and source preservation audit

## Remote chronology and scope

The A2-name branch search was paged through 537 names and an empty final page with no cursor. This includes author revisions, referee copies, external assessments, response/publication/work branches and A2 geometry branches. Name exhaustion is not represented as a byte-level mathematical audit of every branch. A2 geometry reviews were not used as A2-DYN evidence.

The most recent substantive report actually specific to the remote complete A2-DYN article is `f01482035a0b945b50f1f9c30f30ef35077558dc`, report blob `9c68b0e8b31cd196c732514a29ebd44d95964243`. It directly follows v115 `31792379408c5ace2c09284c2eb22d2331023433` and reviews v114–v115. Its full 34,571-byte native report is retained. The v112 controlling report remains a historical dependency. The v113 workflow-only branch is not used as a theorem-bearing manuscript; v114's documentation successor is not a new mathematical source.

## Latest complete local source recovered rather than discarded

The later cross-flight, angular-source and uniform-growth local manuscripts had actual native sources and build evidence but no confirmed remote publication. The last of them is local commit `dbaa43bc597dd1b8d25e3fe18ae73d538f33240b`, repository tree `203c3bc79de989f01e044dfa3024c6f06d339b09`, paper tree `977c51bbc9da6bfbc704db3263026cb01ebc5957`. It descends locally from angular `b02dda2593285ec23cdb1c5e9897b2fa3c7d51b3`, itself following cross-flight `ad757baa0a854a8f1a4b5791210e7ae35410ab35`. That local ancestry is not asserted to be the remote Git ancestry.

The actual 131,928,954-byte latest archive was retrieved with SHA-256 `cc916a9f606eea9e511190f8825f2abc9d4b64bba37c5bff172c4f1427a7de4f`. Its real Git bundle was cloned, the exact local commit and tree were checked, and the complete 70-page native source was freshly rebuilt this iteration. The bundle's missing default HEAD was handled by checking out the explicit existing dbaa commit, not by inventing a parent.

The full delivery freezes all **2,049 files** of that exact predecessor under `provenance/uniform-frozen`. All bytes matched the Git bundle. The ZIP extraction normalized 24 executable modes; those modes were restored from the actual Git tree, and the reconstructed frozen tree is exactly `977c51bbc9da6bfbc704db3263026cb01ebc5957`. The mode correction changed no content. The original delivery archive, its receipt and its bundle remain preserved independently.

## Current mathematical source

Every numbered proof body 260–283 and the seven original model/interface/audit TeX files is retained byte for byte. The new numbered bodies are 284–285. The active main's introductory presentation is revised; its predecessor's full main is preserved both in the full frozen packet and as the exact `provenance/uniform-main.tex` used by the compact native rebuild. Earlier reports, responses, failures, exact finite diagnostics and inherited source manifests remain in the full preserved packet, including their original preparation-time statements.

## Remote publication is additive

The new branch starts from the real controlling-report commit f014820, not an unproved local remote ancestor. The remote native packet is reconstructed from the existing v115 native tree plus the exact later native proof bodies and current additions. Existing repository paths are not overwritten: only a new A2-DYN paper directory and its dedicated workflow are in scope. The remote parent therefore preserves all older remote papers, review branches, companion sources and their evidence. The full local historical archive is supplied separately, rather than pretending a compact remote native snapshot contains every prior log and binary artifact.

Full reconstruction of the recursively nested v111 archive (`790e627efe3a89a4549123d7e9acacf24089c287`) and a mathematical reread of every historical branch have not been completed. The manifest records this explicitly. Preservation by exact parent ancestry is distinct from a claim that all preserved proofs have been independently revalidated.
