# SPDX-License-Identifier: Apache-2.0
import hashlib,json,shutil,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tooling'))
from validate import ROOT,validate
class ValidationTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'repo';shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('.git','dist','__pycache__'))
 def tearDown(self):self.temp.cleanup()
 def edit(self,path,fn):
  p=self.root/path;o=json.loads(p.read_text());fn(o);p.write_text(json.dumps(o));self.rehash(path)
 def rehash(self,path):
  f=self.root/'asset-manifest.json';m=json.loads(f.read_text());m['files'][path]['sha256']=hashlib.sha256((self.root/path).read_bytes()).hexdigest();f.write_text(json.dumps(m))
 def test_valid(self):self.assertEqual(validate(self.root),[])
 def test_unknown_license(self):
  p=self.root/'asset-manifest.json';m=json.loads(p.read_text());m['files']['README.md']['license']='LicenseRef-Unknown';p.write_text(json.dumps(m));self.assertTrue(validate(self.root))
 def test_unregistered_asset(self):
  (self.root/'artwork/unregistered.svg').write_text('<svg/>');self.assertTrue(validate(self.root))
 def test_changed_import(self):
  p=next((self.root/'catalog/upstream').rglob('*.yml'));p.write_text(p.read_text()+'# edit\n');self.assertTrue(any('Checksum' in e for e in validate(self.root)))
 def test_duplicate_ports(self):
  self.edit('catalog/kaleidoscope/CC0-1.0/devices/generic-server-2u.json',lambda t:t['ports'].append(t['ports'][0].copy()));self.assertTrue(any('Duplicate port' in e for e in validate(self.root)))
 def test_out_of_bounds(self):
  self.edit('catalog/kaleidoscope/CC0-1.0/devices/generic-server-2u.json',lambda t:t['ports'][0]['bounds'].update(x=1001));self.assertTrue(any('out of bounds' in e for e in validate(self.root)))
 def test_active_svg(self):
  path='artwork/kaleidoscope/CC0-1.0/connectors/rj45.svg';p=self.root/path;p.write_text(p.read_text().replace('</svg>','<script>alert(1)</script></svg>'));self.rehash(path);self.assertTrue(any('Unsupported SVG' in e for e in validate(self.root)))
 def test_path_traversal(self):
  self.edit('catalog/kaleidoscope/CC0-1.0/devices/generic-server-2u.json',lambda t:t['faces']['rear'].update(artwork='../outside.svg'));self.assertTrue(any('Unsafe path' in e for e in validate(self.root)))
 def test_false_verified(self):
  self.edit('catalog/kaleidoscope/CC0-1.0/devices/generic-server-2u.json',lambda t:t.update(accuracy='verified'));self.assertTrue(any('needs evidence' in e for e in validate(self.root)))
if __name__=='__main__':unittest.main()
