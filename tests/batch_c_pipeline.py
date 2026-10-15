"""Release-integrity and human-source quality checks for Batch C."""
from pathlib import Path
import sys,json,hashlib,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import canonical,compile_corpus,DATA
from ingest import run
m=json.loads((DATA/'content-manifest.json').read_text())
assert m['count']==77,m['count']
assert m['sampleWordCount']>=24000,m['sampleWordCount']
assert sum(a['blocks'] for a in m['articles'])==258
assert len({a['id'] for a in m['articles']})==77
assert len({a['id'].split('.')[0] for a in m['articles']})==10
originals=['I.1.1','II.1.2','III.1.5','VI.4.2','X.5.10']
assert all(any(x['id']==id for x in m['articles']) for id in originals)
src=ROOT/'content/imports/batch_c_editorial.jsonl'
assert run(src,True)['articles_updated']==0
before={p.name:hashlib.sha256(p.read_bytes()).digest() for p in (DATA/'articles').glob('*.json')}
assert run(src)['articles_updated']==0
assert before=={p.name:hashlib.sha256(p.read_bytes()).digest() for p in (DATA/'articles').glob('*.json')}
res=compile_corpus()
assert res['assets_changed']==0,res
assert res['largest_shard']<48_000,res
assert res['largest_pack']<24_000
for p in (ROOT/'dist').rglob('*'):
 if p.is_file():assert not p.relative_to(ROOT/'dist').as_posix().startswith(('canonical/','scripts/','tests/','content/','data/articles/'))
print(f'PASS Batch C corpus: {m["count"]} original articles, {res["blocks"]} published passages, {m["sampleWordCount"]} genuine narrative words, {res["search_shards"]} search shards; all replay and release safeguards')
