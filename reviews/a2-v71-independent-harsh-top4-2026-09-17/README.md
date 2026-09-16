# A2 v71 — independent harsh referee review

Start with [REFEREE_REPORT.md](REFEREE_REPORT.md). This author-requested AI-assisted report is not a journal commission or proof certificate.

**Recommendation:** do not accept at the requested top-four level on the present exceptional-significance case. The concrete v70 lens-comparison and landing-page requests are closed. No new fatal error or mandatory repair of the examined core is established. The remaining recommendation is explicitly a judgment, not an invented mathematical blocker.

## Pinned revision

Review parent: `0367931ab622f1209ba9c62223d92bc8376e7e14` on `revision/a2-v71-referee-ready-2026-09-17`.

Compiled source: `b0a0c9a42e61422cdf7c82df3fb80bedc0d105af`; manuscript subtree: `8549bb0789d5e6cdce8ae12f70ed7c100f81510b`.

This directory adds a review only. Manuscripts, previous reports, native deliveries, existing branches and repository permissions are unchanged.

## Evidence

[DELIVERY_AUDIT.json](DELIVERY_AUDIT.json) records independent source/hash/raw-mode/Git-tree/input-closure/retention checks, and the full-page automatic native-versus-rebuilt PDF comparison. [AUDIT_EVIDENCE.json](AUDIT_EVIDENCE.json) records scope, tools, actual visual sample and build-log identities. [MATHEMATICAL_CHECKS.json](MATHEMATICAL_CHECKS.json) records finite exact symbolic checks. None is a proof certificate.

## Reproduce

Obtain the native ZIP artifacts from `TrillionniumFoundation/theta-theory`: current artifact **10462291207** (run **35133556116**), previous artifact **10449368306** (run **35105117912**). Name the downloads `current.zip` and `previous.zip`. The current source ZIP is also retained in the reviewed repository under `deliveries/a2-v71/b0a0c9a42e61422cdf7c82df3fb80bedc0d105af/native-source.zip`; the review does not depend on an expiring signed download URL.

Python 3.10+ suffices for the byte/mode/tree/retention audit; PyMuPDF is required only for the optional PDF comparison. Run in this directory:

```sh
python verify_delivery.py --current current.zip --previous previous.zip --output audit.json
```

After that validation, unpack `current.zip` into `native/`, unpack its `native-source.zip` into `frozen/`, and copy `frozen/source/` into a clean `rebuilt/`. In `rebuilt/`, build in this dependency order:

```sh
for entry in two_collision main rigidity; do
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
    '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' "$entry.tex" || exit 1
done
```

From the review directory, compare the products:

```sh
python verify_delivery.py --current current.zip --previous previous.zip \
  --native-dir native --rebuilt-dir rebuilt --output audit-with-build.json
python independent_checks.py > mathematical-checks.json
```

The symbolic checker requires SymPy. It imports no manuscript modules. Different TeX versions may change layout; PDF byte identity is not expected. The automatic comparison reports text and RGB differences, while actual visual inspection remains a separate task. This review used PyMuPDF 1.26.7, SymPy 1.14.0, Latexmk 4.86 and pdfTeX 1.40.26.
