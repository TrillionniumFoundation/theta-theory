#!/usr/bin/env python3
"""Activate exactly eight reviewed source edits; preserve all original objects.

The new proof module and revision documents are ordinary tracked text files.
This script only integrates them and corrects the source ZIP mode writer.
It checks old and new Git blob identities before publishing any source commit.
"""
from pathlib import Path
import hashlib
import json
import subprocess

R=Path('papers/A2-v17-boundary-information-coarsening')
A=R/'history/v68-review-baseline'
EXPECTED={'README.md': '484291f7b5290262a0d711b335b53956d589a2e2', 'main.tex': '395f92f72f394db61c0f095c3b7dd7f69f9c16ab', 'rigidity.tex': 'dbee73b03eb17441d57dc5456fbbd8b6bf67c71c', 'article/00h_abstract_v66.tex': 'cf22fa8dba9de51526ba28003150d58d10a60b43', 'article/00g_contact_synthesis_v66.tex': '3166feebab5b7350c5eec3ed42211be4088472be', 'journal/references_v56.tex': 'a3503e20ee4c8ee9b63a37b732efc604bfab268b', 'v5/references_v43.tex': 'f49f0ac6c31ade4164c93fc529a733cdd7a22ead', 'tools/source_provenance.py': 'ade767f2e0751954c0530b1b9eac002a5038d108'}

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

records=json.loads((A/'SOURCE_MANIFEST.json').read_text())['files']
for name, expected in EXPECTED.items():
    old=(A/name).read_bytes()
    require(blob(old)==records[name]['git_blob'], 'Archived original mismatch: '+name)
    require(blob((R/name).read_bytes()) in (records[name]['git_blob'], expected),
            'Refusing to overwrite unexpected source: '+name)
for name in EXPECTED:
    (R/name).write_bytes((A/name).read_bytes())
for name in ['main.tex','rigidity.tex']:
 p=R/name;s=p.read_text().replace('revision 68','revision 69').replace('A2 v68.','A2 v69.')
 s=s.replace('\\input{article/10d_smooth_contact_rigidity_v68}', '\\input{article/10d_smooth_contact_rigidity_v68}\n\\input{article/10e_sampled_smooth_recovery_v69}')
 if name=='rigidity.tex':s=s.replace('analytic rigidity, unknown lattice', 'smooth statistical recovery, analytic rigidity, unknown lattice')
 p.write_text(s)
p=R/'article/00h_abstract_v66.tex';s=p.read_text();s=s.replace('Actual area-preserving obstacle families', 'Regularized finite endpoint samples yield complete-profile recovery under\nfinite-order smoothness bounds and bounded recording error; a deterministic\npreparation budget includes the exponentially rare acceptance cost.\nActual area-preserving obstacle families');p.write_text(s)
p=R/'article/00g_contact_synthesis_v66.tex';s=p.read_text();marker='\\end{theorem}'
pos=s.index(marker)
s=s[:pos]+r'''
Under the uniform finite-order geometric assumptions of
Section~\ref{sec:v69-sampled-contact}, the same marked experiment also
admits finite-sample recovery.  For fixed confidence, $B$ independent
preparations per phase--offset group, and endpoint recording error at most
$\delta$, a realizable estimator satisfies
\[
 \|\widehat F-F\|_{C^0}\le
 C\{(\log B/B)^\beta+\delta^\gamma\}
\]
with the stated high probability, for positive class-dependent exponents
$\beta,\gamma$ and a logarithmically chosen returning flight number.
The exact confidence dependence, priors, estimator, and exponents are
given in Theorem~\ref{thm:v69-charged-recovery}.  Failures count toward
$B$; no density-derivative observations are assumed.
'''+s[pos:]
s=s.replace('they are not general-period sampling rates inferred from density error.',r'''the earlier alternating-channel rates are not being transferred to a
different observation model.  Section~\ref{sec:v69-sampled-contact}
proves a general fixed-period estimate directly.  An interior kernel
estimate supplies the required $C^m$ density control from finitely many
recorded endpoints.  A measurable minimum-distance comparison stays
inside the realizable image, and a binomial lower-tail estimate accounts
for the exponentially small success probability.  This passage is a
consequence of the relative law and smooth contact inverse, not an
independent claim of a new general density-estimation method.  It also
gives a finite charged test between the actual equal-jet flat tables at
any fixed nonzero profile separation.''')
p.write_text(s)
bib=r'''
\bibitem{GineGuillou2002}
E. Gin\'e and A. Guillou,
Rates of strong uniform consistency for multivariate kernel density
estimators, \emph{Ann. Inst. H. Poincar\'e Probab. Statist.}
\textbf{38} (2002), 907--921.
\href{https://doi.org/10.1016/S0246-0203(02)01128-7}{doi:10.1016/S0246-0203(02)01128-7}.

'''
for name in ['journal/references_v56.tex','v5/references_v43.tex']:
 p=R/name;s=p.read_text().replace('\\end{thebibliography}',bib+'\\end{thebibliography}');p.write_text(s)
p=R/'tools/source_provenance.py';s=p.read_text();s=s.replace('''            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)''','''            # A frozen snapshot is read-only, so filesystem permissions are
            # not the source of truth. Preserve the recorded Git modes (R68-P1).
            mode = (int(manifest['files'][name[len('source/'):]]['mode'], 8)
                    if name.startswith('source/') else 0o100644)
            require(mode in (0o100644, 0o100755), 'Unsupported archive mode: ' + name)
            info.create_system = 3  # Unix permission interpretation in ZIP headers.
            info.external_attr = mode << 16
            archive.writestr(info, data)''');p.write_text(s)
p=R/'article/00g_contact_synthesis_v66.tex'
s=p.read_text().replace('proves the fixed-order finite-flight assertion.  All these proofs are\nincluded below.', 'proves the fixed-order finite-flight assertion.  The finite-preparation\nconclusion is Theorem~\\ref{thm:v69-charged-recovery}, using the\nrealizable selection and interior density estimate in the same section.\nAll these proofs are included below.')
p.write_text(s)
(R/'README.md').write_text('''# A2, revision 69

**Boundary laws and smooth contact rigidity of periodic dispersing billiards**  
Qian Qi — September 16, 2026.

This revision responds to the v68 report frozen at `33bd2164d68cae0b412407c8176440fe8d7eaa9b`. The historical directory name does not identify the current revision.

The principal article is `rigidity.tex`; `main.tex` is the complete technical manuscript; `two_collision.tex` is the retained companion. All inherited proof inputs remain active. The sole added mathematical input, `article/10e_sampled_smooth_recovery_v69.tex`, turns the smooth inverse's differentiated-density premise into finite-sample complete-profile recovery and an all-preparations-charged fixed-period estimate, with bounded endpoint recording error. The v68 smooth uniqueness and flat-family proofs and the corrected curvature stopping recursion are unchanged.

`RESPONSE_TO_REFEREE_V69.md` answers every report disposition and separates mathematical scope from editorial significance. `HISTORICAL_DERIVATION_AUDIT_V69.md` records the sources actually read; `journal/DEPENDENCY_LEDGER_V69.md` locates assumptions and proofs. `LITERATURE_CHECK_V69.md` records the targeted primary-source comparison, not an exhaustive priority search. Originals of every changed inherited file are in `history/v68-review-baseline/`.

Build from a clean committed checkout:

```sh
python3 -B tools/build_revision_v69.py --output-dir /tmp/a2-v69-native
```

The build order is companion, complete manuscript, principal article, with regenerated external references. The native builder retains PDFs, logs, source hashes, input manifests and its complete source ZIP. It now writes each ZIP permission header from the recorded Git mode, including executable scripts; it never infers source permissions from a read-only build snapshot. Python's `ZipFile.extractall` does not restore these bits: use `tools/verify_source_zip_v69.py ARCHIVE --extract NEW_DIRECTORY` for checked mode-faithful extraction.

The mathematical and archival checkers use explicit failures and run under ordinary and optimized Python. Their finite controls and successful builds are not proof certificates or journal decisions. No source, previous report, A1 manuscript or historical delivery is removed.
''')

for name, expected in EXPECTED.items():
    require(blob((R/name).read_bytes())==expected, 'Activated blob mismatch: '+name)
    (R/name).chmod(int(records[name]['mode'],8)&0o777)
subprocess.run(['git','add','--',str(R)],check=True)
tree=subprocess.check_output(['git','write-tree'],text=True).strip()
subtree=subprocess.check_output(['git','rev-parse',tree+':'+str(R)],text=True).strip()
require(subtree=='f75a07322d55fd74852b27a99a85fd18a9c2ee6f',
        'Activated manuscript subtree mismatch: '+subtree)
print('Activated source tree: '+subtree)
