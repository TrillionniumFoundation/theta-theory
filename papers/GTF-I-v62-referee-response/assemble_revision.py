"""Materialize frozen v62 native source from an exact v61 base; no network."""
from pathlib import Path
import base64,hashlib,json,lzma
HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v61-sharp-width'
PAYLOAD='b865510223771941449fa45c87aad5fbc4cf689957cc0655e877861a63a0031a'
INVENTORY='ab699b98b91700ef7b9216e3c5ddf289d8de3beab73cac881c6a5ca6a176f718'
FROZEN={'FROZEN_R40_REPORT.md':'86653eccc8f66078e4eea3e18af3ee6cd4db2af8',
        'FROZEN_R40_PIPELINE_AUDIT.md':'b5140e6665062ef6a5ab49a3af3d6e97ed7466d8'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def safe(name):
    path=Path(name)
    require(not path.is_absolute() and '..' not in path.parts,'Unsafe native path')
    return path
def main():
    parts=sorted((HOME/'assembly').glob('part-*.b64'))
    require(len(parts)==5,'Incomplete native delta')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==48572,'Native delta length mismatch')
    decoder=lzma.LZMADecompressor()
    data=decoder.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(data)<=2000000,'Invalid native delta stream')
    require(hashlib.sha256(data).hexdigest()==PAYLOAD,'Native delta digest mismatch')
    delta=json.loads(data);require(len(delta)==63,'Wrong native delta inventory')
    for name,entry in delta.items():
        target=HOME/safe(name)
        if isinstance(entry,str):text=entry
        else:
            original=BASE/safe(entry['base']);raw=original.read_bytes()
            require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'Base source changed: '+name)
            lines=raw.decode('utf-8').splitlines(keepends=True);chunks=[]
            for op in entry['ops']:
                if isinstance(op,str):chunks.append(op)
                else:
                    i,j=op;require(isinstance(i,int) and isinstance(j,int) and 0<=i<=j<=len(lines),'Invalid copy range')
                    chunks.append(''.join(lines[i:j]))
            text=''.join(chunks)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    raw=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==INVENTORY,'Predecessor inventory changed')
    files=json.loads(raw);require(len(files)==344,'Wrong predecessor native inventory')
    for name,digest in files.items():
        data=(BASE/safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Predecessor changed: '+name)
        target=HOME/'retained-v61'/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    manifest={'predecessor_publication':'2c215579336a253585499328f19a647446445dc4',
              'review_commit':'4a99da0aab823418d95631d5dbbd8e9b8178994d',
              'audit_commit':'02c642d3c08774d2dbaee939ffb2eee57b545f92',
              'review_blob':FROZEN['FROZEN_R40_REPORT.md'],
              'audit_blob':FROZEN['FROZEN_R40_PIPELINE_AUDIT.md'],'files':files}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    for name,blob in FROZEN.items():
        data=(HOME/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob,'Frozen report changed: '+name)
    print(json.dumps({'status':'native-source-materialized','own_delta_files':len(delta),'retained_native_files':344,
                      'frozen_reports':2,'qualification':'not yet run'}))
if __name__=='__main__':main()
