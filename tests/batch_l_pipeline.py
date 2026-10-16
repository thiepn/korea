"""Batch L preserves every published paragraph and compiled canonical architecture."""
from __future__ import annotations
from pathlib import Path
import sys,json,hashlib,subprocess,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_batch_l import build,records,OUTPUT
from ingest import run
from build_corpus import compile_corpus,WORD_RE

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical_json(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
original=json.loads((ROOT/'tests/fixtures/batch_l_prior_bytes.json').read_text())
assert len(original['article_sha256'])==143 and len(original['canonical_sha256'])==15
append={'VIII.1.1','VIII.1.2','VIII.1.5'}
for key,h in original['article_sha256'].items():
 path=ROOT/'data/articles'/f'{key}.json'
 current=json.loads(path.read_text(encoding='utf8'))
 # Baseline HEAD is the exact baseline reconstructed from remote main; independent fixture stores byte-level hashes.
 if key not in append:
  assert sha(path.read_bytes())==h,('Unexpected original article change',key)
 else:
  baseline=original['append_prefix'][key]
  assert len(current['blocks'])==baseline['block_count']+1,key
  assert sha(canonical_json(current['blocks'][:baseline['block_count']]))==baseline['blocks_sha256'],key
  assert sha(canonical_json({k:v for k,v in current.items() if k!='blocks'}))==baseline['identity_sha256'],key
for name,h in original['canonical_sha256'].items():
 assert sha((ROOT/'canonical'/name).read_bytes())==h,name
m=build();assert m['new_articles']==7 and m['deepened_articles']==3
assert m['authored_words']>=9000 and m['anchors']>=18,m
assert all(m['counts'][n]>=2000 for n in ('VIII.1.3','VIII.1.7','VIII.1.9'))
assert run(OUTPUT,True)['articles_updated']==0
rows,_=records();paragraphs=[p for r in rows for b in r['blocks'] for p in b['paragraphs']]
normalize=[' '.join(re.findall(r'\w+',p.casefold())) for p in paragraphs]
assert len(normalize)==len(set(normalize)),'Duplicate newly authored paragraph'
manifest=json.loads((ROOT/'data/content-manifest.json').read_text());articles={a['id']:a for a in manifest['articles']}
assert manifest['count']==150 and manifest['sampleWordCount']==100655
assert sum(a['blocks'] for a in articles.values())==726
assert all(f'VIII.1.{i}' in articles for i in range(1,11))
assert all(articles[f'VIII.1.{i}']['wordCount']>=2000 for i in (3,7,9))
assert sum(len(b.get('evidence',[])) for i in (3,4,6,7,8,9,10) for b in json.loads((ROOT/'data/articles'/f'VIII.1.{i}.json').read_text())['blocks'])==m['anchors']
route=next(x for x in json.loads((ROOT/'data/explore.json').read_text())['collections'] if x['slug']=='opening-korea-treaty-ports-complete')
assert route['ids']==[f'VIII.1.{i}' for i in range(1,11)]
atlas=json.loads((ROOT/'data/atlas.json').read_text());assert len(atlas['events'])==78 and len(atlas['connections'])==116
first=compile_corpus();second=compile_corpus();assert second['assets_changed']==0
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
published=[p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert len(published)==881 and not any(p.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for p in published)
print('PASS Batch L: 143 original texts retained, 15 canonical sources identical, 7 new + 3 append-only, '+str(m['authored_words'])+' original words, '+str(m['anchors'])+' evidence anchors; 881 clean assets')
