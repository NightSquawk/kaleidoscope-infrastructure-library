# SPDX-License-Identifier: Apache-2.0
import hashlib,json
from validate import ROOT,files,safe
p=ROOT/'asset-manifest.json';m=json.loads(p.read_text())
if set(m['files'])!=files(ROOT):raise SystemExit('Register/remove file entries explicitly before refreshing hashes.')
for path,meta in m['files'].items():meta['sha256']=hashlib.sha256(safe(ROOT,path).read_bytes()).hexdigest()
p.write_text(json.dumps(m,indent=2)+'\n');print('Refreshed checksums. Review manifest diff before committing.')
