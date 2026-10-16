"""Batch I exact historical preservation, provenance and stable build checks."""
from pathlib import Path
import json,subprocess,sys,re,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from build_corpus import compile_corpus,canonical
from prepare_batch_i import build
from ingest import run
G=['git','-C',str(R)]
BASE=subprocess.check_output(G+['rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(G+['rev-parse',BASE+'^{tree}'],text=True).strip()=='ec71b237ed22269bb10e79c544f6f3198b032e2f'
oldfiles=subprocess.check_output(G+['ls-tree','-r','--name-only',BASE,'data/articles'],text=True).splitlines()
assert len(oldfiles)==121
for f in oldfiles:
 old=json.loads(subprocess.check_output(G+['show',BASE+':'+f]))
 curr=json.loads((R/f).read_text())
 assert old['id']==curr['id'] and old['title']==curr['title'] and curr['blocks'][:len(old['blocks'])]==old['blocks'],f
 assert old.get('sources',[])==curr.get('sources',[])
for f in subprocess.check_output(G+['ls-tree','-r','--name-only',BASE,'canonical'],text=True).splitlines():
 assert (R/f).read_bytes()==subprocess.check_output(G+['show',BASE+':'+f]),f
stats=build();assert stats=={'new_articles':8,'deepened_articles':6,'authored_words':9821,'new_passages':61,'evidence_anchors':12},stats
assert run(R/'content/imports/batch_i_baekje.jsonl',dry_run=True)['articles_updated']==0
m=json.loads((R/'data/content-manifest.json').read_text());idx={a['id']:a for a in m['articles']}
assert (m['count'],m['sampleWordCount'],sum(a['blocks'] for a in m['articles']))==(129,72819,549)
assert all(f'III.2.{n}' in idx for n in range(1,11))
assert all(idx[id]['wordCount']>=2000 for id in ['III.2.1','III.2.6','III.2.8'])
assert len({p['pack'] for id in ['III.2.1','III.2.6','III.2.8'] for p in idx[id]['chunks']})>=3
assert sum(bool(note) for id in [f'III.2.{n}' for n in [1,3,4,6,7,8,9,10]] for b in json.loads((R/'data/articles'/f'{id}.json').read_text())['blocks'] for note in b.get('evidence',[]))==12
atlas=json.loads((R/'data/atlas.json').read_text());assert len(atlas['events'])==57 and len(atlas['connections'])==74
explore=json.loads((R/'data/explore.json').read_text());assert len(explore['collections'])==17
assert next(x for x in explore['collections'] if x['slug']=='baekje-river-maritime-complete')['ids']==[f'III.2.{n}' for n in range(1,11)]
a=compile_corpus();b=compile_corpus();assert b['assets_changed']==0
assert a['largest_pack']<=24000 and a['largest_shard']<=48000
files=list((R/'dist').rglob('*'));files=[p.relative_to(R/'dist').as_posix() for p in files if p.is_file()]
assert len(files)==679
assert not any(f.startswith(('canonical/','scripts/','tests/','content/','data/articles/')) for f in files)
print('PASS Batch I: 8 new, 6 deepened, 9,821 genuine new words, 3 >=2,000, 12 evidence references; full original preservation, replay, deterministic bounded assets')
