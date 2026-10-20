from pathlib import Path
import hashlib, json, re
R=Path("theta-theory/papers/A2-DYN-marked-boundary-source-author-revision")
p=R/"tools/package_source_manifest.py"
s=p.read_text()
s=s.replace("A third anchor\nbinds every one of the 2,088 actual fdf2603 predecessor files.", "A third anchor\nbinds every one of the 2,088 actual fdf2603 predecessor files. A fourth\nbinds all 2,765 actual 0933e9b predecessor files.")
insert="""FULL_PHYSICAL_ANCHOR_PATH = 'history/FULL_PHYSICAL_SOURCE_ANCHOR.json'
FULL_PHYSICAL_ANCHOR_SHA256 = '93ebe2519b142e2f60a9a5d23dd128ef2a7071001b8c1e24e18d31859ec35912'
"""
s=s.replace("MANIFEST_NAME = 'SOURCE_MANIFEST.json'",insert+"MANIFEST_NAME = 'SOURCE_MANIFEST.json'")
original=s[s.index("def verify_physical_tube_history("):s.index("\ndef excluded(")]
fourth=original.replace("verify_physical_tube_history", "verify_full_physical_history").replace("PHYSICAL_TUBE_ANCHOR", "FULL_PHYSICAL_ANCHOR").replace("fdf2603c8bf422314f199fa431086485a0d1ebb5","0933e9b44f5b0fd1d1a624d37ffd881d352496f8").replace("f5c90ecd279dd116330c5d90fa31cae2b0d6f61e","ff4daf7f42d868bd9b41b0b9fe4033489f99bd21").replace("fdf2603","0933e9b").replace("physical-tube","full-physical-source").replace("2088","2765").replace("215569322","318080854").replace("range(260, 314)","range(260, 316)").replace("260-313","260-315").replace("'active_complete_core_bodies_unchanged': 54","'active_complete_core_bodies_unchanged': 56")
s=s.replace("\ndef excluded(", "\n"+fourth+"\ndef excluded(")
s=s.replace("'complete_physical_tube_predecessor': complete}", "'complete_physical_tube_predecessor': complete, 'complete_full_physical_predecessor': verify_full_physical_history(root)}")
s=s.replace("'schema': 4","'schema': 5").replace("get('schema') != 4","get('schema') != 5").replace("All three literal immutable anchors","All four literal immutable anchors")
s=s.replace("'complete_physical_tube_anchor_sha256': PHYSICAL_TUBE_ANCHOR_SHA256,","'complete_physical_tube_anchor_sha256': PHYSICAL_TUBE_ANCHOR_SHA256,\n        'complete_full_physical_anchor_sha256': FULL_PHYSICAL_ANCHOR_SHA256,")
s=s.replace("    rows = manifest.get('files', [])", "    if manifest.get('complete_full_physical_anchor_sha256') != FULL_PHYSICAL_ANCHOR_SHA256:\n        raise VerificationError('Current manifest has the wrong complete full-physical predecessor anchor')\n    rows = manifest.get('files', [])")
p.write_text(s)
p=R/"tools/validate_revision.py"
s=p.read_text().replace("260--315","260--318").replace("len(cores)==56","len(cores)==59").replace("['active_core_end']==315","['active_core_end']==318").replace("r'core/31[4-5]_'","r'core/31[6-8]_'")
s=s.replace("'check_explicit_optical', 'check_full_physical_source',","'check_explicit_optical', 'check_full_physical_source',\n    'check_marked_source_kernel', 'check_marked_boundary_flux', 'check_cross_curve_distortion',")
s=s.replace("'pdflatex','-interaction", "'pdflatex','-recorder','-interaction")
needle="    final=(target/'main.log').read_text(errors='replace')"
recorder="""    spec = importlib.util.spec_from_file_location('typeset_manifest', ROOT/'tools/package_source_manifest.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected=set(module.tex_closure(ROOT)['reachable_tex_files'])
    actual=set()
    for line in (target/'main.fls').read_text().splitlines():
        if not line.startswith('INPUT '):
            continue
        path=Path(line[6:])
        if not path.is_absolute():
            path=ROOT/path
        try:
            relative=path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if relative.endswith('.tex') and not relative.startswith(('history/', 'build/', 'evidence/')):
            actual.add(relative)
    require(actual==expected, 'Actual compiler recorder does not equal the declared native closure')
"""
s=s.replace(needle,recorder+needle)
s=s.replace("'mathematical_proof_certificate':False,'pages':int(match.group(1)),","'mathematical_proof_certificate':False,'pages':int(match.group(1)),\n        'actual_recorder_native_tex':sorted(actual),'actual_recorder_matches_declared_closure':True,")
p.write_text(s)
p=R/"main.tex"
s=p.read_text().replace("full physical-source author revision","marked boundary-source author revision")
abstract=r"""We study exact return, displacement, collision and physical-time records
in the original triangular Lorentz gas for $R\in[9/20,47/100]$.
A true marked-clearance angular source has a uniform momentum kernel
at every collision, including its positive-side zero-clearance trace.
This gives marked incidence moments below the sharp integrability
threshold two without changing the conditional event.
An exact boundary-flux identity retains the physical normal velocity,
and an optical split at the actual marked foot determines both endpoint
incidence factors. On the specified zero-offset critical components,
a uniform inverse-gradient Taylor cancellation bounds that velocity
geometrically in the mark's endpoint depth. The complete covered
word sum consequently decays after the original collision normalization.
Finally, common-minimum localization compares any two actual records
with the same lifted word and matching interior homogeneity strips.
It gives uniform cross-curve distortion with the exact terminal
incidence, stable and optical factors; a genuine terminal grazing
family proves why that factor must be retained.
All preceding proof bodies, including complete weak-roof and singular
multiplier estimates, remain in the manuscript.
These results advance the original raw pointwise local limit and
four-coordinate inverse problem. Nonzero-offset and uncovered boundary
charges, shallow-source capacity, unrestricted pressure and the final
uniform spectral and conditional interfaces remain explicitly open."""
s=re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}",lambda m:"\\begin{abstract}\n"+abstract+"\n\\end{abstract}",s,flags=re.S)
s=s.replace("All fifty-four complete predecessor core proof bodies 260--313","All fifty-six complete predecessor core proof bodies 260--315")
s=s.replace("the ten exact later bodies 304--313","the twelve exact later bodies 304--315")
s=s.replace("retrieved A2-DYN reports.", "retrieved A2-DYN reports, with the separately recovered original v73\nreport documented in the current source audit.")
start=s.index("\\subsection*{Source succession and the scope of external results}")
end=s.index("The controlling retrieved report,",start)
s=s[:start]+r"""\subsection*{Source succession and the scope of external results}
The complete source parent of this author revision is commit
\texttt{0933e9b4\allowbreak 4f5b0fd1\allowbreak d1a624d3\allowbreak
7ffd881d\allowbreak 352496f8}, with article tree
\texttt{ff4daf7f\allowbreak 42d868bd\allowbreak 9b41b0b9\allowbreak
fe403348\allowbreak 9f99bd21}.
Its complete chain through 315, all 2,765 files and every original
Git blob are fixed by a fourth immutable preservation anchor.
The preceding actual CI run 39229329979 tested source receipt commit
\texttt{228ec6a6\allowbreak 39d4d195\allowbreak a1a8b869\allowbreak
a04dae6f\allowbreak 49fece0e}; its later evidence commit is the parent
above. The current article has its own execution records.
An interrupted prepublication environment did not create a successor
commit. The three new proof bodies were recovered exactly against
their previously fixed hashes; the recovery audit separates those
bytes from newly regenerated execution evidence.
Higher-numbered incomplete source wrappers and qualification workflows
do not determine the mathematical baseline.

"""+s[end:]
s=s.replace("it did not review 277--315", "it did not review 277--318")
s=s.replace("The new full-source and mixed-multiplier proofs use their displayed", "The new marked-kernel, boundary and cross-curve proofs use their displayed")
s=s.replace("\\appendix", "\\input{core/316_marked_clearance_momentum_and_trace}\n\\input{core/317_physical_boundary_flux_and_uniform_cancellation}\n\\input{core/318_full_word_cross_curve_distortion}\n\\appendix",1)
p.write_text(s)
print(json.dumps({"status":"integrated", "source":"exact recovered 316--318; inherited 260--315 unchanged","fourth_anchor_sha256":hashlib.sha256((R/"history/FULL_PHYSICAL_SOURCE_ANCHOR.json").read_bytes()).hexdigest()}))

