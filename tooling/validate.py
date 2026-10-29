# SPDX-License-Identifier: Apache-2.0
"""Dependency-free release gate. Explicit checks are the executable v1 contract."""
import hashlib,json,math,re,sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
IGNORED={'.git','dist','__pycache__'}
def files(root):
 return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and not (set(p.relative_to(root).parts)&IGNORED) and p.name!='asset-manifest.json'}
def safe(root,path):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or not path:raise ValueError('Unsafe path: '+path)
 q=root/p
 if not q.resolve().is_relative_to(root.resolve()):raise ValueError('Path escapes root: '+path)
 if not q.is_file():raise ValueError('Missing file: '+path)
 return q

def validate(root=ROOT):
 errors=[]
 def check(ok,msg):
  if not ok:errors.append(msg)
 try:
  manifest=json.loads((root/'asset-manifest.json').read_text());entries=manifest['files']
  allowed=json.loads((root/'policy/licenses.json').read_text())['allowedLicenses']
  check(manifest['license']=='CC0-1.0','Manifest license mismatch')
  check(set(entries)==files(root),'Manifest coverage differs: '+str(set(entries)^files(root)))
  for path,m in entries.items():
   f=safe(root,path)
   check(m['license'] in allowed,'Unapproved license: '+path)
   safe(root,'LICENSES/'+m['license']+'.txt')
   for k in ['source','revision','copyright','modifications','origin']:check(bool(m.get(k)),'Missing '+k+': '+path)
   check(m['origin'] in ['original','upstream','license-text'],'Unknown origin: '+path)
   if m['origin']=='upstream':
    check(bool(re.fullmatch('[0-9a-f]{40}',m['revision'])),'Upstream revision must be pinned: '+path)
    check(m['source'].startswith('https://'),'Missing source URL: '+path)
   if path.startswith('artwork/third-party/') and path.endswith('.svg'):check(bool(m.get('rightsEvidence')),'Missing rights evidence: '+path)
   for n in m.get('notices',[]):safe(root,n)
   check(hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256'],'Checksum mismatch: '+path)
   if path.endswith('.svg'):
    raw=f.read_text();check('<!DOCTYPE' not in raw.upper() and '<!ENTITY' not in raw.upper(),'Unsafe XML: '+path)
    tree=ET.fromstring(raw)
    for el in tree.iter():
     tag=el.tag.split('}')[-1]
     check(tag in {'svg','title','desc','g','rect','circle','ellipse','path','line','polyline','polygon','text'},'Unsupported SVG element: '+tag)
     for attr,value in el.attrib.items():
      check(not attr.lower().startswith('on') and 'href' not in attr.lower() and 'url(' not in value.lower(),'Active/external SVG content: '+path)
  provenance=json.loads((root/'catalog/upstream/netbox/CC0-1.0/provenance.json').read_text())
  for record in provenance['files']:
   path='catalog/upstream/netbox/CC0-1.0/'+record['path']
   check(hashlib.sha256(safe(root,path).read_bytes()).hexdigest()==record['sha256'],'Upstream provenance checksum mismatch: '+path)
   check(entries[path]['revision']==provenance['revision'],'Upstream revision mismatch: '+path)
  connectors=json.loads((root/'catalog/kaleidoscope/CC0-1.0/connectors.json').read_text())
  for path in connectors.values():safe(root,path)
  ids=set()
  for f in sorted((root/'catalog/kaleidoscope/CC0-1.0/devices').glob('*.json')):
   t=json.loads(f.read_text());name=t['id'];check(name not in ids,'Duplicate template ID');ids.add(name)
   check(t['schemaVersion']==1,'Unsupported schema version')
   check(t['accuracy'] in ['illustrative','verified'],'Invalid accuracy')
   check(t['license']==entries[f.relative_to(root).as_posix()]['license'],'Template license differs from manifest')
   d=t['dimensions']
   for key in ['widthMm','depthMm','heightMm']:check(isinstance(d[key],(float,int)) and math.isfinite(d[key]) and d[key]>0,'Invalid dimension '+key)
   u=d['heightU'];check(isinstance(u,(int,float)) and math.isfinite(u) and u>=0 and u*2==int(u*2),'Invalid U height')
   check((u==0)==(t['mounting']=='vertical-0u'),'0U mounting mismatch')
   check(t['mounting'] in ['rack','vertical-0u'],'Invalid mounting')
   if t['accuracy']=='verified':check(bool(t.get('evidence')),'Verified template needs evidence')
   for face,detail in t['faces'].items():
    check(face in ['front','rear'],'Unsupported face');safe(root,detail['artwork'])
    check(detail['viewBox'][:2]==[0,0] and all(v>0 for v in detail['viewBox'][2:]),'Invalid viewBox')
    art=ET.parse(root/detail['artwork']).getroot()
    check(list(map(float,art.attrib['viewBox'].split()))==detail['viewBox'],'SVG/template viewBox mismatch')
   pids=set();boxes={}
   for p in t['ports']:
    check(p['id'] not in pids,'Duplicate port ID: '+name);pids.add(p['id'])
    check(p['connector'] in connectors,'Unknown connector')
    check(p['role'] in ['network','power','video','usb','pass-through','console'],'Unknown role')
    check(p['face'] in t['faces'],'Unknown face')
    b=p['bounds'];x,y,w,h=[b[k] for k in ['x','y','width','height']];vw,vh=t['faces'][p['face']]['viewBox'][2:]
    check(all(isinstance(v,(int,float)) and math.isfinite(v) for v in [x,y,w,h]) and x>=0 and y>=0 and w>0 and h>0 and x+w<=vw and y+h<=vh,'Port out of bounds: '+name+'/'+p['id'])
    for ox,oy,ow,oh in boxes.setdefault(p['face'],[]):check(not(x<ox+ow and x+w>ox and y<oy+oh and y+h>oy),'Overlapping port bounds: '+name)
    boxes[p['face']].append((x,y,w,h))
 except (KeyError,TypeError,ValueError,OSError,ET.ParseError) as e:errors.append(str(e))
 return errors
if __name__=='__main__':
 errors=validate();print('\n'.join(errors) if errors else 'PASS: licensing, provenance, checksums, SVG safety and template geometry');sys.exit(bool(errors))
