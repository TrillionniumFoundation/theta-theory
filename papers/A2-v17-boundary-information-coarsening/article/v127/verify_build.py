from pathlib import Path
import json
import fitz

ROOT = Path(__file__).resolve().parent
log = (ROOT / "geometry.log").read_text(encoding="utf-8", errors="replace")
pdf = ROOT / "geometry.pdf"
statement = (ROOT / "parts/01b-boundary-atlas.tex").read_text(encoding="utf-8")
proof = (ROOT / "parts/09b-boundary-atlas-proofs.tex").read_text(encoding="utf-8")
rees = (ROOT / "parts/09a-rees-specialization.tex").read_text(encoding="utf-8")
cert = ROOT / "evidence/BOUNDARY_ATLAS_CERTIFICATES.json"

checks = {
    "pdf_exists": pdf.exists() and pdf.stat().st_size > 100_000,
    "no_undefined_references": "undefined references" not in log.lower(),
    "no_undefined_citations": "undefined citations" not in log.lower(),
    "no_latex_error": "! LaTeX Error" not in log,
    "global_depth_theorem_present": "Finite all-corank depth and multiplication" in statement,
    "mixed_kernel_atlas_present": "Corank-two mixed-kernel atlas" in statement,
    "corank_three_theorem_present": "Projection corank three" in statement,
    "corank_four_theorem_present": "Projection corank four and the Jacobian quartic" in statement,
    "d5_proof_present": "Laplace expansion" in proof and "d^5" in proof,
    "standard_dnc_positioning": "standard" in rees.lower() and "FultonIntersection" in rees,
    "boundary_certificates_exist": cert.exists(),
}
if cert.exists():
    data = json.loads(cert.read_text(encoding="utf-8"))
    checks["boundary_character_checks"] = bool(
        data.get("wedge6_sym2_GL4_decomposition")
        and data.get("corank3_GL3_character_identities")
        and data.get("b0_exact_delta_cubed")
    )
else:
    checks["boundary_character_checks"] = False

if pdf.exists():
    doc = fitz.open(pdf)
    checks["pdf_pages"] = len(doc)
    checks["pdf_page_floor"] = len(doc) >= 30
else:
    checks["pdf_pages"] = 0
    checks["pdf_page_floor"] = False

out = {
    "revision": 127,
    "checks": checks,
    "ok": all(v for k, v in checks.items() if k != "pdf_pages"),
}
(ROOT / "evidence" / "BUILD_RECEIPT.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
if not out["ok"]:
    raise SystemExit(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
