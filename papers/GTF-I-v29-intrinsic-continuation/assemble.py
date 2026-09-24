#!/usr/bin/env python3
"""Reversible assembly of the new theorem spine and unchanged predecessor body."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v28-causal-response'
EXPECTED_BLOB='f4a82fe0ec5b294bfa9a8d8a299e8bb97fb6f442'
EXPECTED_MODULES={'integer-revelation.tex': '3de2046a003cf47296f2af12ce45443d67a0402ec4f2f72c686bd8144bf807b7', 'two-preparation-family.tex': 'dc2d0d2d8d8eb350695475ec178b625c48eef75a278cc63ccea3fd6f2b4b8ecf', 'foundations.tex': 'd03a6d18c14a4b5971c4f8ff40718622739b68796b3da17cc3bf9bc6d7d76c4f', 'physical-improvement.tex': '19254d25767ae7e928913a902a30db564ebe99c0c62dd234d9a1d5fdde83cab7', 'joint-revelation.tex': '3acd0a5a4fd38b21cfbd3571882881cd5260adee604680df603f5b16b07655ad', 'controlled-dual.tex': '5386724853685ec361165b7b28ff676a59ab9519c4534a112f63fc7fe39110a3', 'saddle-realization.tex': '89b68b67231fda47a736c8acb706bfeaef0a2b1dde0c2a510db144e8ea9eee0e', 'two-preparation-saddle.tex': 'b70eeb2a863af2f4b700cc5251dca963fe3b255f4a33a13e0d40f8497fc409a7', 'validation-order.tex': '6c1517cddeec9299f86917b9e929432b939d66b0ca2c6bc4f5cb965b8d115255', 'consumer-transfer.tex': '7b67e2fe2696f26320545b6f6227701014717cf20cad8b24f7ac2cd66e90b821', 'preparation-localization.tex': '1ff6ceb94d5bdc0a96cd2dc2b4e16a1da026c523cf6d71727466ba3854130b60', 'physical-noise-law.tex': '8d502c20c81a6f9e17a994918706d9d0beceb0efad3e4ee3a5f7d27219aa12c8', 'physical-bridge.tex': 'ab54a2712f41874f13e98128a1578ef76d494081c5e37a988143ac0674625930', 'positive-noise-saddle.tex': '7ce0bf9c0b1f7d5d939374011259b841b964b0ffd748c99aefbf533469ffccfd', 'controlled-memory.tex': '4acd4ae2f62aebc498c5b2be2fb364a81b9e232113a221d316432b24fb4a62bc', 'facial-scheduling.tex': 'c6274a64f171f8ec430a18a20cf0048394b0754a59b30834434f6e70535225a0', 'marked-minimax.tex': 'e1228e123a62f8df54235502e584fbb50cd80b23d3059b08601acf6ef02f3d51', 'exact-memory.tex': '4db8a2830f39d975ae22431e4de1b7f3a665d3f2775141cb0605137559fcb331'}
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def need(test:bool,message:str)->None:
    if not test:raise RuntimeError(message)
raw=(O/'main.tex').read_bytes()
need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==EXPECTED_BLOB,'Predecessor main Git blob mismatch')
text=raw.decode()
start=text.index('\\input{foundations}')
end=text.index('\\begin{thebibliography}')
body=text[start:end]
preamble=text[:text.index('\\begin{abstract}')]
preamble=preamble.replace('\\usepackage[T1]{fontenc}',r'\usepackage{mathrsfs}'+'\n'+r'\usepackage[T1]{fontenc}')
a=preamble.index('\\title[');b=preamble.index('\\author{',a)
preamble=preamble[:a]+r"""\title[Intrinsic continuation geometry]{General Theta Foundations I:\\
Intrinsic Continuation Geometry and Causal Memory}
"""+preamble[b:]
import re
preamble=re.sub(r'\\date\{[^}]*\}',lambda m:r'\date{September 24, 2026. Revision 29}',preamble)
modules=['intrinsic-continuation','tensor-continuation','streaming-access','contact-application','literature-theorems']
newcore=''.join('\\input{'+name+'}\n' for name in modules)
header=r"""
\clearpage
\appendix
\renewcommand{\thesection}{A.\arabic{section}}
\section*{Supporting foundations and physical proofs}
\label{sec:retained29}
The following sections preserve the substantive mathematical body of
revision 28. They supply the exact saddles, microscopic model,
validation-order proofs, general causal foundations, and quantitative
consumers used above. Earlier local scope statements describe the
individual results in which they occur; the new classification and
streaming theorems are stated in Sections~\ref{sec:intrinsic29}--\ref{sec:contact29}.
All predecessor theorem labels and all mathematical proofs remain
available in this manuscript. The current introduction and theorem
hierarchy replace repeated roadmap prose, not the supporting mathematics.

% BEGIN BYTE-PRESERVED V28 MATHEMATICAL BODY
"""
footer='\n% END BYTE-PRESERVED V28 MATHEMATICAL BODY\n'
bibliography=text[end:]
bibliography=bibliography.replace('\\end{thebibliography}',(H/'new-references.tex').read_text()+'\n\\end{thebibliography}')
assembled=preamble+(H/'introduction.tex').read_text()+'\n'+newcore+header+body+footer+bibliography
(H/'main.tex').write_text(assembled)
recovered=assembled.split('% BEGIN BYTE-PRESERVED V28 MATHEMATICAL BODY\n',1)[1].split(footer,1)[0]
need(recovered==body,'Reversibility check failed')
for name,expected in EXPECTED_MODULES.items():
    need(sha((O/name).read_bytes())==expected,'Pinned module mismatch '+name)
    need((O/name).read_bytes()==(H/name).read_bytes(),'Copied mathematical module changed '+name)
manifest={'schema':'gtf29.assembly/1','predecessor_main_git_blob':EXPECTED_BLOB,
 'predecessor_main_sha256':sha(raw),'preserved_mathematical_body_sha256':sha(body.encode()),
 'preserved_mathematical_body_lines':len(body.splitlines()),'unchanged_mathematical_modules':EXPECTED_MODULES,
 'native_main_sha256':sha(assembled.encode()),'new_core_modules':modules,
 'reversible_body_preservation':True,'presentation':'New theorem spine; unchanged substantive predecessor body in supporting appendices.'}
(H/'ASSEMBLY_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'assembly':'verified','unchanged_modules':len(EXPECTED_MODULES)},sort_keys=True))
