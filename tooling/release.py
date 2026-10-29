# SPDX-License-Identifier: Apache-2.0
import zipfile,json,hashlib
from validate import ROOT,validate
errors=validate()
if errors:raise SystemExit('\n'.join(errors))
out=ROOT/'dist';out.mkdir(exist_ok=True)
paths=sorted(json.loads((ROOT/'asset-manifest.json').read_text())['files'])+['asset-manifest.json']
with zipfile.ZipFile(out/'kaleidoscope-infrastructure-library.zip','w',zipfile.ZIP_DEFLATED) as z:
 for path in paths:
  i=zipfile.ZipInfo('kaleidoscope-infrastructure-library/'+path,date_time=(2026,1,1,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o644<<16;z.writestr(i,(ROOT/path).read_bytes())
f=out/'kaleidoscope-infrastructure-library.zip';print(f);print('SHA256',hashlib.sha256(f.read_bytes()).hexdigest())
