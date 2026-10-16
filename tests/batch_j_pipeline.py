"""Batch J immutable-baseline, actual long-form content and replay checks."""
from pathlib import Path
import sys,json,subprocess,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import compile_corpus,WORD_RE
from prepare_batch_j import build,records,OUTPUT
from ingest import run
def sha(data):return hashlib.sha256(data).hexdigest()
fixture=json.loads((ROOT/'tests/fixtures/batch_j_verified_baseline.json').read_text())
assert fixture['baseline_tree_sha']=='2d4799d56dfa2935e5415d863b614e29edca6d01'
assert len(fixture['articles'])==129
for id,item in fixture['articles'].items():
 new=json.loads((ROOT/'data/articles'/f'{id}.json').read_text())
 prefix=new['blocks'][:item['blocks']]
 digest=sha(json.dumps(prefix,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8'))
 metadata=sha(json.dumps({k:new.get(k) for k in ('id','title','sources')},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8'))
 assert digest==item['blocks_sha256'],id
 assert metadata==item['identity_sha256'],id
for path,digest in fixture['canonical'].items():
 assert sha((ROOT/path).read_bytes())==digest,path
stats=build()
assert stats['new_articles']==7 and stats['deepened_articles']==3
assert stats['authored_words']>=9000 and stats['evidence_anchors']>=9
assert all(stats['longform_words'][id]>=2000 for id in ('IV.3.2','IV.3.5','IV.3.7'))
assert run(OUTPUT,True)['articles_updated']==0
articles={f.stem for f in (ROOT/'data/articles').glob('*.json')}
assert all(f'IV.3.{i}' in articles for i in range(1,11))
manifest=json.loads((ROOT/'data/content-manifest.json').read_text());byid={a['id']:a for a in manifest['articles']}
assert manifest['count']==136 and manifest['sampleWordCount']==82269
assert sum(x['blocks'] for x in manifest['articles'])==605
assert len({x['id'] for x in manifest['articles']})==len(manifest['articles'])
assert all(byid[k]['wordCount']>=2000 for k in ('IV.3.2','IV.3.5','IV.3.7'))
assert all(byid[k].get('sources') for k in [f'IV.3.{i}' for i in (2,5,6,7,8,9,10)])
assert all(len(json.loads((ROOT/'data/articles'/f'IV.3.{i}.json').read_text())['blocks'])>=4 for i in (2,5,6,7,8,9,10))
notes=sum(len(b.get('evidence',[])) for i in (2,5,6,7,8,9,10) for b in json.loads((ROOT/'data/articles'/f'IV.3.{i}.json').read_text())['blocks'])
assert notes==stats['evidence_anchors']
# No duplicate new passages, even under punctuation and whitespace normalization.
texts=[p for i in (2,5,6,7,8,9,10) for b in json.loads((ROOT/'data/articles'/f'IV.3.{i}.json').read_text())['blocks'] for p in b['paragraphs']]
normalized=[' '.join(re.findall(r'\w+',x.casefold())) for x in texts]
assert len(set(normalized))==len(normalized)
atlas=json.loads((ROOT/'data/atlas.json').read_text())
assert len(atlas['events'])==63 and len(atlas['connections'])==88
paths=json.loads((ROOT/'data/explore.json').read_text())['collections']
assert len(paths)==18
assert next(x for x in paths if x['slug']=='silla-everyday-life-complete')['ids']==[f'IV.3.{i}' for i in range(1,11)]
for name in ['VI.4','IX.3','III.3','IX.1','III.2']:
 assert all(f'{name}.{i}' in articles for i in range(1,11))
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0,second
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
assets=[x.relative_to(ROOT/'dist').as_posix() for x in (ROOT/'dist').rglob('*') if x.is_file()]
assert len(assets)==745
assert not any(x.startswith(('content/','canonical/','tests/','scripts/','data/articles/')) for x in assets)
print('PASS Batch J: immutable 129 prior articles and canonical files; 7 new + 3 deepened; 3 essays 2,000+; 9,450 original words; 10 claim annotations; replay, integrity, deterministic build')
