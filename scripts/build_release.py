#!/usr/bin/env python3
"""Build the deployable KOREA Phase 1 site using allowlisted public runtime assets."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
for path in ('index.html', 'app.js', 'exploration.js', 'styles.css', 'data/architecture.json', 'data/content-manifest.json', 'data/explore.json', 'data/search-index.json'):
    src = ROOT / path
    assert src.is_file(), f'Missing runtime asset {path}'
    target = DIST / path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)
manifest = json.loads((ROOT/'data/content-manifest.json').read_text())
for block in sorted((ROOT/'data/blocks').glob('*.json')):
    target = DIST/'data/blocks'/block.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(block, target)
# Explicitly prohibit project-internal sources and development scripts in published output.
assert not (DIST/'canonical').exists()
assert not (DIST/'scripts').exists()
assert not (DIST/'tests').exists()
assert not (DIST/'data/articles').exists()
assert not list(DIST.rglob('*.md'))
allfiles = sorted(str(p.relative_to(DIST)) for p in DIST.rglob('*') if p.is_file())
print(f'KOREA public build: {len(allfiles)} files; {sum((DIST/f).stat().st_size for f in allfiles):,} bytes')
print('\n'.join('  '+p for p in allfiles))
