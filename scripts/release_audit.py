#!/usr/bin/env python3
"""Check which exact release files may appear in the public directory."""
from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parent.parent
pub=root/'dist'
required={'index.html','styles.css','app.js','data/architecture.json','data/content-manifest.json'}
files={str(p.relative_to(pub)) for p in pub.rglob('*') if p.is_file()}
assert required<=files,required-files
assert len(files)==33, len(files)
assert len([f for f in files if f.startswith('data/blocks/')])==28
assert all(f in required or f.startswith('data/blocks/') for f in files),sorted(files-required)
assert not (pub/'canonical').exists()
assert not (pub/'scripts').exists()
assert not (pub/'tests').exists()
assert not (pub/'data/articles').exists()
assert (pub/'index.html').read_bytes()==(root/'index.html').read_bytes()
assert (pub/'app.js').read_bytes()==(root/'app.js').read_bytes()
assert (pub/'styles.css').read_bytes()==(root/'styles.css').read_bytes()
for f in files:
    assert (pub/f).stat().st_size>0
print('PASS: exact 33 asset allowlist; 28 blocks; no canonical/development sources in dist')
