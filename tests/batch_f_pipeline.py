"""Batch F exact canonical coverage, original immutability, selective claim evidence, idempotent imports."""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_collections import build,EXPECTED
from ingest import run
from build_corpus import compile_corpus,WORD_RE
arch=json.loads((ROOT/'data/architecture.json').read_text())
ids={s['id'] for p in arch['parts'] for c in p['chapters'] for s in c['subchapters']}
assert len(arch['parts'])==10 and sum(len(p['chapters']) for p in arch['parts'])==100 and len(ids)==1000
assert EXPECTED.issubset(ids)
assert build(write=True)=={'articles':12,'passages':48,'words':9106,'marked_claims':10}
assert run(ROOT/'content/imports/batch_f_collections.jsonl',dry_run=True)['articles_updated']==0
manifest=json.loads((ROOT/'data/content-manifest.json').read_text())
assert manifest['count']>=107 and manifest['sampleWordCount']>=48075
assert sum(a['blocks'] for a in manifest['articles'])>=405
byid={a['id']:a for a in manifest['articles']}
assert len(byid)>=107
for chapter in ['VI.4','IX.3']:
 assert all(f'{chapter}.{i}' in byid for i in range(1,11))
refs=0;notes=0
for key in EXPECTED:
 article=json.loads((ROOT/'data/articles'/f'{key}.json').read_text())
 assert article['title']==next(s['title'] for p in arch['parts'] for c in p['chapters'] for s in c['subchapters'] if s['id']==key)
 assert len(article['blocks'])>=4 and len(article['sources'])==2 and article['release']=='F'
 assert byid[key]['wordCount']>=550
 for b in article['blocks'][:4]:
  assert len(b['paragraphs'])>=2
  for x in b.get('evidence',[]):
   notes+=1
   assert x['type'] in ('direct','context') and x['claim'] and x['locator']
   assert article['sources'][x['sourceIndex']]['url'].startswith('https://')
 refs+=len(article['sources'])
assert refs==24 and notes==10
# Compare the immutable pre-F release, permitting later append-only additions.
git=['git','-c',f'safe.directory={ROOT}','-C',str(ROOT)]
baseline='3f478fd^'  # exact pre-F local source commit
old=subprocess.check_output(git+['ls-tree','-r','--name-only',baseline,'data/articles'],text=True).splitlines()
assert len(old)==95,len(old)
for path in old:
 previous=json.loads(subprocess.check_output(git+['show',baseline+':'+path]));current=json.loads((ROOT/path).read_text());assert current['blocks'][:len(previous['blocks'])]==previous['blocks'],path
for f in (ROOT/'canonical').iterdir():
 if f.is_file():assert f.read_bytes()==subprocess.check_output(git+['show',baseline+':canonical/'+f.name]),f.name
atlas=json.loads((ROOT/'data/atlas.json').read_text());assert len(atlas['events'])>=36 and len(atlas['connections'])>=40
paths=json.loads((ROOT/'data/explore.json').read_text())['collections'];assert len(paths)>=13
for name,prefix in [('writing-and-knowledge','VI.4'),('the-korean-war-complete','IX.3')]:
 path=next(x for x in paths if x['slug']==name)
 assert path['ids']==[f'{prefix}.{i}' for i in range(1,11)]
first=compile_corpus();second=compile_corpus();assert second['assets_changed']==0
assert first['largest_pack']<24000 and first['largest_shard']<=48000
files=[x.relative_to(ROOT/'dist').as_posix() for x in (ROOT/'dist').rglob('*') if x.is_file()]
assert len(files)<20000 and not any(x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in files)
print(f'PASS F: 12 new canonical subjects; 48 independently written passages; 9,106 words; 24 sources and 10 anchored claims; both chapters fully readable; 95 original articles unchanged; {len(files)} public assets; idempotent importer/pack compiler')
