"""Batch O exact-baseline article/canonical preservation, sourced prose and replay evidence."""
from __future__ import annotations
import json,hashlib,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from prepare_batch_o import build,NEW,APPEND,LONG,OUT
from ingest import run
from build_corpus import compile_corpus
sha=lambda raw:hashlib.sha256(raw).hexdigest()
enc=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
prior=json.loads((R/'tests/fixtures/batch_o_prior_bytes.json').read_text())
assert prior['baseline_main']=='7baf2f930498ec8ec595d58a50d43c1ab815fb6a'
assert len(prior['articles'])==166 and len(prior['canonical'])==15
for name,digest in prior['canonical'].items():assert sha((R/'canonical'/name).read_bytes())==digest,name
for key,row in prior['articles'].items():
 p=R/'data/articles'/f'{key}.json';curr=json.loads(p.read_text())
 if key not in APPEND:assert sha(p.read_bytes())==row['sha256'],('older article mutated',key)
 else:
  assert len(curr['blocks'])>row['blocks']
  assert sha(enc(curr['blocks'][:row['blocks']]))==row['prefix_sha256'],('old block mutated',key)
  assert sha(enc({k:v for k,v in curr.items() if k!='blocks'}))==row['identity_sha256'],('metadata mutated',key)
metrics=build();assert metrics['new_articles']==17 and metrics['append_only_articles']==9
assert metrics['authored_words']==22930 and metrics['new_passages']==101 and metrics['evidence_anchors']==20
assert all(metrics['words_by_article'][k]>=2000 for k in LONG)
assert run(OUT,True)['articles_updated']==0,'import replay modified articles'
rows=[json.loads(line) for line in OUT.read_text().splitlines() if line]
assert {r['id'] for r in rows}==NEW|APPEND
paragraphs=[p for r in rows for b in r['blocks'] for p in b['paragraphs']]
normalized=[' '.join(re.findall(r'\w+',p.casefold())) for p in paragraphs]
assert len(normalized)==len(set(normalized)), 'duplicate paragraphs'
manifest=json.loads((R/'data/content-manifest.json').read_text());topics={x['id']:x for x in manifest['articles']}
assert manifest['count']==183 and manifest['sampleWordCount']==141656
assert sum(x['blocks'] for x in topics.values())==937
for chapter in ('V.5','VIII.9'):
 assert all(f'{chapter}.{i}' in topics for i in range(1,11))
explore=json.loads((R/'data/explore.json').read_text())
assert len(explore['collections'])==24
for chap,slug in [('V.5','goryeo-religion-complete'),('VIII.9','independence-movements-complete')]:
 route=next(x for x in explore['collections'] if x['slug']==slug)
 assert route['ids']==[f'{chap}.{i}' for i in range(1,11)]
atlas=json.loads((R/'data/atlas.json').read_text());assert len(atlas['events'])==108 and len(atlas['connections'])==163
aliases=json.loads((R/'content/atlas/search-aliases.json').read_text())
assert all(k in aliases for k in NEW)
assert sum(len(b.get('evidence',[])) for k in NEW for b in json.loads((R/'data/articles'/f'{k}.json').read_text())['blocks'])==20
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0 and first['largest_pack']<=24000 and first['largest_shard']<=48000
files=[p.relative_to(R/'dist').as_posix() for p in (R/'dist').rglob('*') if p.is_file()]
assert len(files)==1109 and not any(x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in files)
print('PASS Batch O: 166 prior articles, 15 canonical files, two complete Chapters, +22930 authored words, 101 passages, 20 source anchors, replay, content hashes')
