from pathlib import Path
import json
import fitz

ROOT = Path(__file__).resolve().parent
tex = (ROOT / "frontmatter.tex").read_text(encoding="utf-8")
log = (ROOT / "geometry.log").read_text(encoding="utf-8", errors="replace")
pdf = ROOT / "geometry.pdf"

checks = {
    "pdf_exists": pdf.exists() and pdf.stat().st_size > 100_000,
    "no_undefined_references": "undefined references" not in log.lower(),
    "no_undefined_citations": "undefined citations" not in log.lower(),
    "no_latex_error": "! LaTeX Error" not in log,
    "abstract_mathcal_escaped": "(mathcal" not in tex and "[\n mathcal" not in tex,
    "rees_theorem_present": "Canonical Rees specialization" in (ROOT / "parts/01a-rees-specialization.tex").read_text(encoding="utf-8"),
}
if pdf.exists():
    doc = fitz.open(pdf)
    checks["pdf_pages"] = len(doc)
    checks["pdf_page_floor"] = len(doc) >= 25
else:
    checks["pdf_pages"] = 0
    checks["pdf_page_floor"] = False

out = {
    "revision": 126,
    "checks": checks,
    "ok": all(v for k, v in checks.items() if k != "pdf_pages"),
}
(ROOT / "evidence" / "BUILD_RECEIPT.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
if not out["ok"]:
    raise SystemExit(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
