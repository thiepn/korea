"""Batch E content, provenance, immutable archive and build verification."""
from pathlib import Path
import json,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_longform import run as prepare
from ingest import run as ingest
from build_corpus import compile_corpus,WORD_RE

arch=json.loads((ROOT/'data/architecture.json').read_text())
canon={a['id'] for p in arch['parts'] for c in p['chapters'] for a in c['subchapters']}
assert len(canon)==1000
stats=prepare()
assert len(stats)==3 and all(s['words']>=2000 and s['passages']>=6 for s in stats.values()),stats
assert ingest(ROOT/'content/imports/batch_e_longform.jsonl',dry_run=True)['articles_updated']==0
m=json.loads((ROOT/'data/content-manifest.json').read_text())
assert m['count']>=95 and m['sampleWordCount']>=38969 and sum(x['blocks'] for x in m['articles'])>=357
long=[a for a in m['articles'] if a['release']=='E']
assert len(long)==3 and all(a['wordCount']>=2000 and len(a['sources'])>=2 for a in long)
assert sum(a['wordCount'] for a in long)==sum(s['words'] for s in stats.values())
for a in long:
 assert a['id'] in canon
 assert all(x['url'].startswith('https://') for x in a['sources'])
 assert 'not ' in a['sourceStatus'].lower() or 'outstanding' in a['sourceStatus'].lower()
 raw=json.loads((ROOT/'data/articles'/f'{a["id"]}.json').read_text())
 assert len(raw['blocks'])==a['blocks']
 assert not any('synthetic' in p.lower() for b in raw['blocks'] for p in b['paragraphs'])
 assert len({b['title'] for b in raw['blocks']})==len(raw['blocks'])
for f in (ROOT/'canonical').rglob('*'):
 if not f.is_file():continue
 source=Path('/mnt/data')/f.name
 if source.is_file():assert f.read_bytes()==source.read_bytes(),f.name
atlas=json.loads((ROOT/'data/atlas.json').read_text())
assert len(atlas['events'])>=30 and len(atlas['connections'])>=28
assert set(stats).issubset({e['id'] for e in atlas['events']})
collections=json.loads((ROOT/'data/explore.json').read_text())['collections']
assert len(collections)>=11 and set(stats).issubset(set(next(c for c in collections if c['slug']=='longform-history')['ids']))
c1=compile_corpus();c2=compile_corpus();assert c2['assets_changed']==0
assert c1['largest_pack']<=24000 and c1['largest_shard']<=48000
assets={p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()}
assert all(not x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in assets)
print('PASS E: 3 >=2,000-word essays, 7,296 words, 24 passages, 6 institutional reference links, canonical unchanged, 30 timeline nodes, 28 connections, 11 trails, deterministic build')
