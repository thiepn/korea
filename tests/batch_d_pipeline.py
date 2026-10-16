"""Batch D source corpus and release integrity, including before/after immutability."""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import compile_corpus
from ingest import run
from prepare_editorial import prepare
manifest=json.loads((ROOT/'data/content-manifest.json').read_text())
arch=json.loads((ROOT/'data/architecture.json').read_text())
atlas=json.loads((ROOT/'data/atlas.json').read_text())
assert len(arch['parts'])==10 and sum(map(lambda p:len(p['chapters']),arch['parts']))==100
assert manifest['count']>=92 and manifest['sampleWordCount']>=31673 and sum(a['blocks'] for a in manifest['articles'])>=333
assert len(atlas['events'])>=27 and len(atlas['connections'])>=24
new=[a for a in manifest['articles'] if a['release']=='D'];assert len(new)==15 and all(a['blocks']>=5 and a['wordCount']>=420 for a in new)
prepared=ROOT/'content/imports/batch_d_deep.jsonl'
assert run(prepared,True)['articles_updated']==0,'Importer must replay without rewriting sources'
all_ids={s['id'] for p in arch['parts'] for c in p['chapters'] for s in c['subchapters']}
assert all(a['id'] in all_ids for a in manifest['articles'])
for e in atlas['events']:assert e['id'] in all_ids
for item in atlas['connections']:assert item['from'] in all_ids and item['to'] in all_ids
c1=compile_corpus();c2=compile_corpus();assert c2['assets_changed']==0,c2
assert c1['largest_pack']<=24_000 and c1['largest_shard']<=48_000
for candidate in ROOT.glob('canonical/*'):
 source=Path('/mnt/data')/candidate.name
 if source.is_file() and candidate.suffix!='.xlsx': assert hashlib.sha256(candidate.read_bytes()).digest()==hashlib.sha256(source.read_bytes()).digest(),candidate.name
public={p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()}
assert 'data/atlas.json' in public
assert not any(s.startswith(('content/','canonical/','tests/','scripts/')) for s in public)
print(f'PASS Batch D backwards-compatibility: {manifest["count"]} articles, {manifest["sampleWordCount"]} words, {len(atlas["events"])} events, {len(atlas["connections"])} connections')
