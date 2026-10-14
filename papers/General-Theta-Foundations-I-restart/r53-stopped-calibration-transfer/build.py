#!/usr/bin/env python3
"""Reuse the hash-pinned read-only retained builder; only publication names change."""
from pathlib import Path
import hashlib
previous=Path(__file__).resolve().parent.parent/'r52-stopped-experiment/build.py'
data=previous.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob!='cf67a0bb3b8932b46c2db98f7115928dbaa2b677':
    raise RuntimeError('retained build dependency differs from pinned R52 source')
source=data.decode().replace('R52','R53').replace('r52','r53')
source=source.replace('r51-causal-acquisition','r52-stopped-experiment').replace('R51','R52')
source=source.replace('Companion_CausalAcquisition','Companion_StoppedExperiment')
source=source.replace("dest=target/PAPER_DIR/'r53-stopped-experiment'","dest=target/PAPER_DIR/'r53-stopped-calibration-transfer'")
exec(compile(source,str(previous)+' [R53 publication names]','exec'),globals())
