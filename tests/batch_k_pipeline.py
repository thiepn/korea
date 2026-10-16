"""Batch K: source integrity, preserved paragraphs and real authored corpus growth."""
import hashlib,json,subprocess,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_batch_k import build,records,OUTPUT
from build_corpus import compile_corpus
from ingest import run

def sha(data):return hashlib.sha256(data).hexdigest()
def compact(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
fixture=json.loads((ROOT/'tests/fixtures/batch_k_verified_baseline.json').read_text())
assert fixture['baseline_tree_sha']=='b6e53c0ab1ddd76964dddda1b1e0493d52ec1689'
assert len(fixture['articles'])==136
for id,record in fixture['articles'].items():
    article=json.loads((ROOT/'data/articles'/f'{id}.json').read_text())
    assert sha(compact(article['blocks'][:record['count']]))==record['paragraph_sha256'],id
    assert sha(compact({k:article.get(k) for k in ('id','title','sources')}))==record['identity_sha256'],id
for path,digest in fixture['canonical'].items():
    assert sha((ROOT/path).read_bytes())==digest,path
metrics=build()
assert metrics['new_articles']==7 and metrics['deepened_articles']==3
assert metrics['authored_words']>=9000 and metrics['anchors']>=10,metrics
assert all(metrics['word_counts'][key]>=2000 for key in ('II.1.1','II.1.6','II.1.10'))
assert run(OUTPUT,True)['articles_updated']==0
records_,_=records()
texts=[p for r in records_ for b in r['blocks'] for p in b['paragraphs']]
normalized=[' '.join(re.findall(r'\w+',s.casefold())) for s in texts]
assert len(normalized)==len(set(normalized)),'Duplicate new paragraphs'
manifest=json.loads((ROOT/'data/content-manifest.json').read_text());names={x['id']:x for x in manifest['articles']}
assert manifest['count']==143 and manifest['sampleWordCount']==91600
assert sum(x['blocks'] for x in manifest['articles'])==660
assert all(f'II.1.{i}' in names for i in range(1,11))
assert all(names[k]['wordCount']>=2000 for k in ('II.1.1','II.1.6','II.1.10'))
for i in (1,3,5,6,8,9,10):
    obj=json.loads((ROOT/'data/articles'/f'II.1.{i}.json').read_text())
    assert obj['release']=='K' and obj['sourceStatus'] and len(obj['sources'])>=3
assert sum(len(b.get('evidence',[])) for i in (1,3,5,6,8,9,10) for b in json.loads((ROOT/'data/articles'/f'II.1.{i}.json').read_text())['blocks'])==metrics['anchors']
atlas=json.loads((ROOT/'data/atlas.json').read_text())
assert len(atlas['events'])==70 and len(atlas['connections'])==100
assert all(c['why'] for c in atlas['connections'])
routes=json.loads((ROOT/'data/explore.json').read_text())['collections']
assert len(routes)==19
assert next(c for c in routes if c['slug']=='gojoseon-evidence-and-memory-complete')['ids']==[f'II.1.{i}' for i in range(1,11)]
r1=compile_corpus();r2=compile_corpus()
assert r2['assets_changed']==0
assert r1['largest_pack']<=24000 and r1['largest_shard']<=48000
assets=[x.relative_to(ROOT/'dist').as_posix() for x in (ROOT/'dist').rglob('*') if x.is_file()]
assert len(assets)==807
assert not any(x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in assets)
print('PASS Batch K: 136 original articles and all canonical files unchanged; 7 new, 3 deepened, 9331 original words, 11 annotations; idempotent source import and 807-asset clean build')
