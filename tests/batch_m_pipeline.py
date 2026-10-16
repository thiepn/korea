"""Batch M preservation, source-based corpus, and replay checks; independent of local Git history."""
from pathlib import Path
import sys,json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from prepare_batch_m import build,OUT,NEW_IDS,APPEND_IDS
from ingest import run
from build_corpus import compile_corpus
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
base=json.loads((ROOT/'tests/fixtures/batch_m_prior_bytes.json').read_text())
assert len(base['article_sha256'])==150 and len(base['canonical_sha256'])==15
for key,digest in base['article_sha256'].items():
 path=ROOT/'data/articles'/f'{key}.json';current=json.loads(path.read_text())
 if key not in APPEND_IDS:assert sha(path.read_bytes())==digest,('source overwritten',key)
 else:
  prefix=base['append_prefix'][key];n=prefix['block_count']
  assert len(current['blocks'])==n+2,('incorrect append count',key)
  assert sha(canon(current['blocks'][:n]))==prefix['blocks_sha256'],('old passages changed',key)
  assert sha(canon({k:v for k,v in current.items() if k!='blocks'}))==prefix['identity_sha256'],('metadata rewritten',key)
for name,digest in base['canonical_sha256'].items():
 assert sha((ROOT/'canonical'/name).read_bytes())==digest,('canonical modified',name)
metrics=build()
assert metrics['new_articles']==8 and metrics['deepened_articles']==2 and metrics['authored_words']==9000,metrics
assert metrics['anchors']==14 and all(metrics['words_by_article'][id]>=2000 for id in ['VII.5.1','VII.5.4','VII.5.9'])
assert run(OUT,True)['articles_updated']==0,'Replaying imported content must be idempotent'
rows=[json.loads(line) for line in OUT.read_text().splitlines() if line]
paragraphs=[p for r in rows for b in r['blocks'] for p in b['paragraphs']]
normalized=[' '.join(re.findall(r'\w+',p.casefold())) for p in paragraphs]
assert len(normalized)==len(set(normalized)),'Duplicate new paragraphs'
manifest=json.loads((ROOT/'data/content-manifest.json').read_text());published={a['id']:a for a in manifest['articles']}
assert manifest['count']==158 and manifest['sampleWordCount']==109655,manifest['sampleWordCount']
assert sum(a['blocks'] for a in published.values())==784
assert all(f'VII.5.{i}' in published for i in range(1,11))
assert all(published[k]['wordCount']>=2000 for k in ['VII.5.1','VII.5.4','VII.5.9'])
route=next(x for x in json.loads((ROOT/'data/explore.json').read_text())['collections'] if x['slug']=='late-joseon-family-complete')
assert route['ids']==[f'VII.5.{i}' for i in range(1,11)]
atlas=json.loads((ROOT/'data/atlas.json').read_text())
assert len(atlas['events'])==86 and len(atlas['connections'])==132
assert sum(len(b.get('evidence',[])) for k in NEW_IDS for b in json.loads((ROOT/'data/articles'/f'{k}.json').read_text())['blocks'])==14
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0 and first['largest_pack']<=24000 and first['largest_shard']<=48000
published_assets=[p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert len(published_assets)==931 and not any(p.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for p in published_assets)
print('PASS Batch M: 150 original articles, 15 canonical files preserved; 8 new + 2 append-only; 9,000 genuine words; 14 evidence anchors; 931 clean published assets')
