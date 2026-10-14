#!/usr/bin/env python3
"""Read-only R57 build; retains the complete unchanged R56 chain."""
from pathlib import Path
import hashlib
previous=Path(__file__).resolve().parent.parent/'r52-stopped-experiment/build.py'
data=previous.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob!='cf67a0bb3b8932b46c2db98f7115928dbaa2b677':raise RuntimeError('pinned retained builder changed')
source=data.decode().replace('R52','R57').replace('r52','r57')
source=source.replace('r51-causal-acquisition','r56-balanced-task-transfer').replace('R51','R56')
source=source.replace('Companion_CausalAcquisition','Companion_BalancedTaskTransfer')
source=source.replace("dest=target/PAPER_DIR/'r57-stopped-experiment'","dest=target/PAPER_DIR/'r57-role-aware-transfer'")
source=source.replace("target=prepared/PAPER_DIR/'r56-balanced-task-transfer/review_inputs/R32_EXTERNAL_REFEREE_REPORT.md'\n            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)", "target=prepared/PAPER_DIR/'r56-balanced-task-transfer/review_inputs/R53_EXTERNAL_REFEREE_REPORT.md'\n            require(git_hash('blob',target.read_bytes())=='9c86a6fe706ad991765720f48fb78dde6b597a2b','retained R56 review pin')")
exec(compile(source,str(previous)+' [R57 publication names]','exec'),globals())
