"""Render source-bound R80 PDFs; rendering alone is not visual inspection."""
from pathlib import Path
import argparse,hashlib,json,subprocess
from PIL import Image,ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args();B=args.build.resolve();O=args.out.resolve()
if O.exists() and any(O.iterdir()):raise RuntimeError('Use a fresh render directory')
O.mkdir(parents=True,exist_ok=True)
a=json.loads((B/'BUILD_RECEIPT.json').read_text())
if a['status']!='PASS' or not a['source_commit_verified']:raise RuntimeError('An actual strict source-bound PASS is required')
index=json.loads((B/'THEOREM_INDEX.json').read_text());loc={r['label']:r for r in index['statements']}
selected={'manuscript':[1,3,9,19,33,68,73]+list(range(20,33)),
 'supplement':list(range(1,8))+[196]+[loc[k]['page'] for k in ['thm:face','thm:memory-certificate','thm:compact-risk','thm:primitive-fallback']],
 'companion':[1,12,25,37]}
receipt={'schema':'theta.r80.pdf-render-record.v1','source_commit':a['declared_source_commit'],
 'scope':'Actual renders produced for separately recorded visual inspection. Generation alone is not a visual verdict.',
 'render_command':'pdftoppm -png; contact inputs at30dpi; readable individual pages at110dpi',
 'poppler':subprocess.run(['pdftoppm','-v'],capture_output=True,text=True).stderr.splitlines()[0],
 'pillow':Image.__version__,'documents':[],'rendered_files':[]}
for d in a['documents']:
    pdf=B/d['file'];name=d['document'];raw=pdf.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=d['sha256']:raise RuntimeError('PDF hash differs')
    temp=O/('thumbnails-'+name);temp.mkdir()
    subprocess.run(['pdftoppm','-r','30','-png',str(pdf),str(temp/'page')],check=True,capture_output=True)
    pages=sorted(temp.glob('page-*.png'))
    if len(pages)!=d['pages']:raise RuntimeError('Raster page count differs')
    for start in range(0,len(pages),24):
        group=pages[start:start+24];w,h=275,385;sheet=Image.new('RGB',(w*6,h*4),'#dedede');draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(group):
            im=Image.open(p).convert('RGB');im.thumbnail((w-12,h-34));x=(i%6)*w+(w-im.width)//2;y=(i//6)*h+25;sheet.paste(im,(x,y));draw.text(((i%6)*w+10,(i//6)*h+6),f'{name} page {start+i+1}',fill='black')
        sheet.save(O/f'{name}-contact-{start//24+1:02d}.png',optimize=True)
    detail=sorted(set(selected[name]))
    if not all(1<=p<=d['pages'] for p in detail):raise RuntimeError('Selected page out of range')
    for page in detail:
        subprocess.run(['pdftoppm','-r','110','-png','-singlefile','-f',str(page),'-l',str(page),str(pdf),str(O/f'{name}-page-{page:03d}')],check=True,capture_output=True)
    receipt['documents'].append({'document':name,'pdf':d['file'],'pdf_sha256':d['sha256'],'all_pages_rendered':len(pages),'detail_pages':detail})
for p in sorted(O.glob('*.png')):
    data=p.read_bytes();receipt['rendered_files'].append({'file':p.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(O/'RENDER_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'all_pages':sum(d['all_pages_rendered'] for d in receipt['documents']),'detail_pages':sum(len(d['detail_pages']) for d in receipt['documents']),'contact_and_detail_images':len(receipt['rendered_files']),'source_commit':a['declared_source_commit']}))
