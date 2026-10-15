#!/usr/bin/env python3
"""Allowlist release artifact builder. Never publish editable sources or governance."""
from pathlib import Path
import json,shutil
from build_corpus import compile_corpus
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
compile_corpus()
subprocess.run([sys.executable,str(ROOT/'scripts/build_exploration.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build_atlas.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/validate.py')],check=True)
if DIST.exists():shutil.rmtree(DIST)
DIST.mkdir()
for name in ['index.html','app.js','exploration.js','content-platform.js','reader-window.js','styles.css','data/architecture.json','data/content-manifest.json','data/explore.json','data/atlas.json','data/search/catalog.json','data/search/shard-map.json']:
 src=ROOT/name
 if not src.is_file():raise FileNotFoundError(name)
 dest=DIST/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
for folder in ['data/packs','data/search/shards']:
 for src in sorted((ROOT/folder).glob('*.json')):
  dest=DIST/folder/src.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
allfiles=[p.relative_to(DIST).as_posix() for p in DIST.rglob('*') if p.is_file()]
assert all(not x.startswith(('canonical/','scripts/','tests/','data/articles/','data/blocks/','content/')) and not x.endswith(('.md','.py','.jsonl')) for x in allfiles)
assert (DIST/'data/packs').exists()
print(f'PASS release: {len(allfiles)} public runtime files; {sum((DIST/x).stat().st_size for x in allfiles):,} bytes')
