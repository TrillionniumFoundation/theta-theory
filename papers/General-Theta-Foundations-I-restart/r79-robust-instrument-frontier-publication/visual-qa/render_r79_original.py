from pathlib import Path
import subprocess,json,hashlib,math
from PIL import Image,ImageOps,ImageDraw
B=Path('/workspace/scratch/b8655e579b01/r79_verified_build');O=Path('/workspace/scratch/b8655e579b01/r79_visual_qa');O.mkdir(exist_ok=True)
a=json.loads((B/'BUILD_RECEIPT.json').read_text())
if a['status']!='PASS':raise RuntimeError('Strict source-bound build must pass first')
index=json.loads((B/'THEOREM_INDEX.json').read_text());loc={r['label']:r for r in index['statements']}
selected={'manuscript':[1,3,7,9,10,11,12,13,14,15,16,17,18,19,20,24,40,54,59],
          'supplement':[1,190]+[loc[k]['page'] for k in ['thm:face','thm:memory-certificate','thm:compact-risk','thm:primitive-fallback'] if k in loc],
          'companion':[1,12,25,37]}
receipt={'source_commit':a['git_identity']['head'],'scope':'Generated page renders for separate visual inspection; generation alone is not a visual verdict.','documents':[],'rendered_files':[]}
for d in a['documents']:
 pdf=B/d['file'];name=d['document'];temp=O/('thumbnails-'+name);temp.mkdir(exist_ok=True)
 subprocess.run(['pdftoppm','-r','30','-png',str(pdf),str(temp/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 pages=sorted(temp.glob('page-*.png'))
 if len(pages)!=d['pages']:raise RuntimeError('Wrong raster page count')
 for start in range(0,len(pages),24):
  group=pages[start:start+24];w,h=275,385;sheet=Image.new('RGB',(w*6,h*4),'#dedede');draw=ImageDraw.Draw(sheet)
  for i,p in enumerate(group):
   im=Image.open(p).convert('RGB');im.thumbnail((w-12,h-34));x=(i%6)*w+(w-im.width)//2;y=(i//6)*h+25;sheet.paste(im,(x,y));draw.text(((i%6)*w+10,(i//6)*h+6),f'{name} page {start+i+1}',fill='black')
  target=O/f'{name}-contact-{start//24+1:02d}.png';sheet.save(target,optimize=True)
 for page in sorted(set(selected[name])):
  subprocess.run(['pdftoppm','-r','110','-png','-singlefile','-f',str(page),'-l',str(page),str(pdf),str(O/f'{name}-page-{page:03d}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 receipt['documents'].append({'document':name,'pdf':d['file'],'pdf_sha256':d['sha256'],'all_pages_rendered':len(pages),'detail_pages':sorted(set(selected[name]))})
for p in sorted(O.glob('*.png')):receipt['rendered_files'].append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'RENDER_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'all_pages':sum(d['all_pages_rendered'] for d in receipt['documents']),'contact_and_detail_images':len(receipt['rendered_files']),'source_commit':a['git_identity']['head']}))
