#!/usr/bin/env python3
"""R54 read-only build via a hash-pinned inherited implementation."""
from pathlib import Path
import hashlib
previous=Path(__file__).resolve().parent.parent/'r52-stopped-experiment/build.py'
data=previous.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob!='cf67a0bb3b8932b46c2db98f7115928dbaa2b677':raise RuntimeError('pinned retained builder changed')
source=data.decode().replace('R52','R54').replace('r52','r54')
source=source.replace('r51-causal-acquisition','r53-stopped-calibration-transfer').replace('R51','R53')
source=source.replace('Companion_CausalAcquisition','Companion_StoppedCalibrationTransfer')
source=source.replace("dest=target/PAPER_DIR/'r54-stopped-experiment'","dest=target/PAPER_DIR/'r54-predictable-geometry'")
exec(compile(source,str(previous)+' [R54 publication names]','exec'),globals())
