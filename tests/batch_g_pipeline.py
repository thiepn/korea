"""Batch G: proof of all previous narrative text, complete Chapter and provenance."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from prepare_batch_g import build,NEW,DEEP
from ingest import run,is_contiguous_replay
from build_corpus import compile_corpus,WORD_RE,canonical
GIT=['git','-c',f'safe.directory={ROOT}','-C',str(ROOT)]
BASELINE_OPTIONS=['c747bdd5fd2c7ec55e6f2891dd58540d704c7ae1','3f478fd2a185f21563303c499860535f09017aa6']
BASELINE=next((sha for sha in BASELINE_OPTIONS if subprocess.run(GIT+['cat-file','-e',sha+'^{commit}'],capture_output=True).returncode==0),None)
if not BASELINE:raise RuntimeError('Batch F source baseline unavailable; fetch history to run preservation comparison')
old_files=subprocess.check_output(GIT+['ls-tree','-r','--name-only',BASELINE,'data/articles'],text=True).splitlines()
assert len(old_files)==107,len(old_files)
old_origins={}
for f in old_files:
 previous=json.loads(subprocess.check_output(GIT+['show',BASELINE+':'+f]))
 current=json.loads((ROOT/f).read_text())
 assert current['id']==previous['id'] and current['title']==previous['title']
 assert current['blocks'][:len(previous['blocks'])]==previous['blocks'],f
 assert current.get('sources',[])==previous.get('sources',[]),f
 assert all(current.get(k)==previous.get(k) for k in ['description','kicker','sourceStatus','release']),f
 old_origins[current['id']]=len(previous['blocks'])
for f in (ROOT/'canonical').iterdir():
 if f.is_file():assert f.read_bytes()==subprocess.check_output(GIT+['show',BASELINE+':canonical/'+f.name]),f
assert build(write=True)=={'new':7,'append':12,'passages':40,'words':6523,'direct_claims':7}
assert run(ROOT/'content/imports/batch_g_collections.jsonl',dry_run=True)['articles_updated']==0
# An earlier batch must remain replay-safe even after additional later passages.
a={'title':'first','paragraphs':['old'],'evidence':[]}
b={'title':'second','paragraphs':['later'],'evidence':[]}
c={'title':'third','paragraphs':['newest'],'evidence':[]}
assert is_contiguous_replay([a,b,c],[a,b])
assert is_contiguous_replay([a,b,c],[b])
assert not is_contiguous_replay([a,b,c],[a,c])
manifest=json.loads((ROOT/'data/content-manifest.json').read_text())
assert manifest['count']>=114 and manifest['sampleWordCount']>=54598
assert sum(x['blocks'] for x in manifest['articles'])>=445
ids={a['id'] for a in manifest['articles']};canonical_titles=canonical()
assert set(NEW).issubset(ids)
assert all(f'III.3.{i}' in ids for i in range(1,11))
assert len(canonical_titles)==1000
for key in NEW:
 a=json.loads((ROOT/'data/articles'/f'{key}.json').read_text());assert a['title']==canonical_titles[key]
 assert len(a['blocks'])==4 and len(a['sources'])==2
 assert sum(len(WORD_RE.findall(p)) for b in a['blocks'] for p in b['paragraphs'])>=525
 assert sum(len(b.get('evidence',[])) for b in a['blocks'])==1
 for b in a['blocks']:
  for e in b.get('evidence',[]):assert 0<=e['sourceIndex']<len(a['sources']) and e['claim'] and e['locator']
for key in DEEP:
 a=json.loads((ROOT/'data/articles'/f'{key}.json').read_text())
 assert len(a['blocks'])>=old_origins[key]+1
assert set(a['id'] for a in manifest['articles'])==ids
atlas=json.loads((ROOT/'data/atlas.json').read_text());paths=json.loads((ROOT/'data/explore.json').read_text())['collections']
assert len(atlas['events'])>=43 and len(atlas['connections'])>=51 and len(paths)>=14
assert next(p for p in paths if p['slug']=='silla-rise-complete')['ids']==[f'III.3.{i}' for i in range(1,11)]
first=compile_corpus();second=compile_corpus();assert second['assets_changed']==0
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
assert all(not x.relative_to(ROOT/'dist').as_posix().startswith(('canonical/','tests/','scripts/','content/','data/articles/')) for x in (ROOT/'dist').rglob('*') if x.is_file())
print('PASS G 7 new Silla subjects, 12 append-only deepened articles; 6,523 original words; all original 107 article passages and canonical sources byte-identical; 7 references, 43 atlas entries, 51 relations; deterministic packaging')
