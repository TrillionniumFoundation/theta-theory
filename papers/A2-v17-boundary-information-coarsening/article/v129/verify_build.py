from pathlib import Path
import json
import fitz

ROOT = Path(__file__).resolve().parent
log = (ROOT / "geometry.log").read_text(encoding="utf-8", errors="replace")
pdf = ROOT / "geometry.pdf"
statement = (ROOT / "parts/01b-boundary-atlas.tex").read_text(encoding="utf-8")
proof = (ROOT / "parts/09b-boundary-atlas-proofs.tex").read_text(encoding="utf-8")
relative = (ROOT / "parts/09c-relative-primary-specialization.tex").read_text(encoding="utf-8")
intro = (ROOT / "parts/01-introduction.tex").read_text(encoding="utf-8")
cert = ROOT / "evidence/BOUNDARY_ATLAS_CERTIFICATES.json"
generic = ROOT / "evidence/GENERIC_BOUNDARY_CERTIFICATES.json"

checks = {
    "pdf_exists": pdf.exists() and pdf.stat().st_size > 100_000,
    "no_undefined_references": "undefined references" not in log.lower(),
    "no_undefined_citations": "undefined citations" not in log.lower(),
    "no_latex_error": "! LaTeX Error" not in log,
    "native_v128_introduction": "Revision 128" in intro,
    "universal_det_completion": "Universal symmetric-power determinant completion" in statement,
    "effective_pieri_proof": "Effective Cauchy--Pieri multiplication" in proof,
    "relative_assassin_proof": "Relative primary signatures and specialization laws" in relative and "relative assassin" in relative.lower(),
    "rankdrop_primary_table": "Generic primary signatures for every" in relative,
    "specialization_laws": "orbit closure and specialization laws" in relative.lower(),
    "boundary_certificates_exist": cert.exists(),
    "generic_boundary_certificates_exist": generic.exists(),
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

if generic.exists():
    data = json.loads(generic.read_text(encoding="utf-8"))
    checks["generic_slice_checks"] = bool(
        data.get("effective_pieri_horizontal_four_strip")
        and len(data.get("mixed_kernel_generic_slices", [])) == 7
        and len(data.get("rankdrop_generic_slices", [])) == 9
    )
else:
    checks["generic_slice_checks"] = False

if pdf.exists():
    doc = fitz.open(pdf)
    checks["pdf_pages"] = len(doc)
    checks["pdf_page_floor"] = len(doc) >= 40
else:
    checks["pdf_pages"] = 0
    checks["pdf_page_floor"] = False

out = {
    "revision": 128,
    "checks": checks,
    "ok": all(v for k, v in checks.items() if k != "pdf_pages"),
}
(ROOT / "evidence" / "BUILD_RECEIPT.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
if not out["ok"]:
    raise SystemExit(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
