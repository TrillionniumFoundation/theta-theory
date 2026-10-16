#!/usr/bin/env python3
"""Read-only R58 build; retains the complete unchanged R57 and R56 chain."""
from pathlib import Path
import hashlib
previous=Path(__file__).resolve().parent.parent/'r52-stopped-experiment/build.py'
data=previous.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob!='cf67a0bb3b8932b46c2db98f7115928dbaa2b677':raise RuntimeError('pinned retained builder changed')
source=data.decode().replace('R52','R58').replace('r52','r58')
source=source.replace('r51-causal-acquisition','r57-role-aware-transfer').replace('R51','R57')
source=source.replace('Companion_CausalAcquisition','Companion_RoleAwareTransfer')
source=source.replace("dest=target/PAPER_DIR/'r58-stopped-experiment'","dest=target/PAPER_DIR/'r58-reference-stability'")
source=source.replace("target=prepared/PAPER_DIR/'r57-role-aware-transfer/review_inputs/R32_EXTERNAL_REFEREE_REPORT.md'\n            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)", "target=prepared/PAPER_DIR/'r57-role-aware-transfer/review_inputs/R56_EXTERNAL_REFEREE_REPORT.md'\n            require(git_hash('blob',target.read_bytes())=='15c692a39c17a34a408e2979f049c87b804179f8','retained R57 review pin')")
exec(compile(source,str(previous)+' [R58 publication names]','exec'),globals())
