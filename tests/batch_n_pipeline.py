"""Source-preserving Batch N checks; usable on standalone archive/exact checkout."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from prepare_batch_n import build,NEW_IDS,APPEND_IDS,LONG_IDS,OUTPUT
from ingest import run
from build_corpus import compile_corpus
sha=lambda raw:hashlib.sha256(raw).hexdigest()
canon=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
prior=json.loads((R/'tests/fixtures/batch_n_prior_bytes.json').read_text())
assert len(prior['articles'])==158 and len(prior['canonical'])==15
for name,digest in prior['canonical'].items():
 assert sha((R/'canonical'/name).read_bytes())==digest,('canonical drift',name)
for key,row in prior['articles'].items():
 p=R/'data/articles'/f'{key}.json';current=json.loads(p.read_text())
 if key not in APPEND_IDS:assert sha(p.read_bytes())==row['sha256'],('prior article changed',key)
 else:
  n=row['blocks'];assert len(current['blocks'])==n+2
  assert sha(canon(current['blocks'][:n]))==row['prefix_sha256'],('old passages changed',key)
  assert sha(canon({k:v for k,v in current.items() if k!='blocks'}))==row['identity_sha256'],('prior metadata changed',key)
metrics=build();assert metrics['new_articles']==8 and metrics['deepened_articles']==2
assert metrics['authored_words']==9071 and metrics['new_passages']==52 and metrics['evidence_anchors']==14
assert all(metrics['words_by_article'][i]>=2000 for i in LONG_IDS)
assert run(OUTPUT,True)['articles_updated']==0,'Import should be replay-safe'
rows=[json.loads(x) for x in OUTPUT.read_text().splitlines() if x]
assert {x['id'] for x in rows}==NEW_IDS|APPEND_IDS
paragraphs=[p for row in rows for block in row['blocks'] for p in block['paragraphs']]
normalized=[' '.join(re.findall(r'\w+',p.casefold())) for p in paragraphs]
assert len(normalized)==len(set(normalized)), 'repeated narrative paragraph'
manifest=json.loads((R/'data/content-manifest.json').read_text());topics={x['id']:x for x in manifest['articles']}
assert manifest['count']==166 and manifest['sampleWordCount']==118726
assert sum(x['blocks'] for x in topics.values())==836
assert all(f'V.1.{i}' in topics for i in range(1,11))
assert all(topics[i]['wordCount']>=2000 for i in LONG_IDS)
explore=json.loads((R/'data/explore.json').read_text())
route=next(c for c in explore['collections'] if c['slug']=='goryeo-foundation-complete')
assert route['ids']==[f'V.1.{i}' for i in range(1,11)]
atlas=json.loads((R/'data/atlas.json').read_text());assert len(atlas['events'])==93 and len(atlas['connections'])==143
aliases=json.loads((R/'content/atlas/search-aliases.json').read_text());assert all(f'V.1.{i}' in aliases for i in range(1,11))
assert sum(len(b.get('evidence',[])) for key in NEW_IDS for b in json.loads((R/'data/articles'/f'{key}.json').read_text())['blocks'])==14
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0 and first['largest_pack']<=24000 and first['largest_shard']<=48000
files=[x.relative_to(R/'dist').as_posix() for x in (R/'dist').rglob('*') if x.is_file()]
assert len(files)==980 and not any(n.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for n in files)
print('PASS Batch N pipeline: 158 prior articles, 15 canonical files preserved, +8 articles, +52 passages, +9071 authored words, 14 sourced claims, replay/asset invariants')
