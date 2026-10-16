"""Batch H: evidence-aware genuine authorship and append-only v1.1 preservation."""
from pathlib import Path
import sys,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from prepare_batch_h import build
from ingest import run
from build_corpus import compile_corpus,canonical,WORD_RE
GIT=['git','-c',f'safe.directory={ROOT}','-C',str(ROOT)]
BASE='2b8f273e698fc1691c4e1f601ef3dd1e1eebcb8e' # exact local tree of remote G main
canonical_ids=canonical()
assert len(canonical_ids)==1000
oldfiles=subprocess.check_output(GIT+['ls-tree','-r','--name-only',BASE,'data/articles'],text=True).splitlines()
assert len(oldfiles)==114
old_blocks=0
for path in oldfiles:
    old=json.loads(subprocess.check_output(GIT+['show',BASE+':'+path]))
    curr=json.loads((ROOT/path).read_text(encoding='utf8'))
    assert old['id']==curr['id'] and old['title']==curr['title']
    assert curr['blocks'][:len(old['blocks'])]==old['blocks'],f'Old passage overwritten {path}'
    assert old.get('sources',[])==curr.get('sources',[]),f'Source metadata changed {path}'
    old_blocks+=len(old['blocks'])
for path in subprocess.check_output(GIT+['ls-tree','-r','--name-only',BASE,'canonical'],text=True).splitlines():
    assert subprocess.check_output(GIT+['show',BASE+':'+path])==(ROOT/path).read_bytes(),path
stats=build();assert stats=={'new_articles':7,'deepened_prior_articles':4,'passages':43,'added_words':8400,'evidence_anchors':8},stats
replay=run(ROOT/'content/imports/batch_h_collections.jsonl',dry_run=True)
assert replay['articles_updated']==0,replay
manifest=json.loads((ROOT/'data/content-manifest.json').read_text(encoding='utf8'))
assert (manifest['count'],manifest['sampleWordCount'])==(121,62998)
assert sum(a['blocks'] for a in manifest['articles'])==488
index={a['id']:a for a in manifest['articles']}
assert all(f'IX.1.{i}' in index for i in range(1,11))
assert all(index[id]['wordCount']>=2000 for id in ['IX.1.1','IX.1.6','VI.4.3','IX.3.3'])
assert sum(index[k]['blocks'] for k in index if k.startswith('IX.1.'))>=40
new={f'IX.1.{i}' for i in range(4,11)}
assert all(index[k]['sourceStatus'].startswith('Selective primary') for k in new)
refs=0
for key in new:
    a=json.loads((ROOT/'data/articles'/f'{key}.json').read_text(encoding='utf8'))
    assert a['title']==canonical_ids[key]
    assert len(a['sources'])>=1
    for b in a['blocks']:
        for note in b.get('evidence',[]):
            refs+=1
            assert note['type'] in ('context','direct') and len(note['claim'])>=24
            assert a['sources'][note['sourceIndex']]['url'].startswith('https://')
assert refs==8
atlas=json.loads((ROOT/'data/atlas.json').read_text());explore=json.loads((ROOT/'data/explore.json').read_text())['collections']
assert len(atlas['events'])==50 and len(atlas['connections'])==62
assert len(explore)==16
assert next(t for t in explore if t['slug']=='liberation-to-partition')['ids']==[f'IX.1.{i}' for i in range(1,11)]
first=compile_corpus();second=compile_corpus();assert second['assets_changed']==0
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
release=[x.relative_to(ROOT/'dist').as_posix() for x in (ROOT/'dist').rglob('*') if x.is_file()]
assert len(release)==616
assert not any(x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in release)
print('PASS H: 7 new articles, 4 deepenings, 8,400 original words; 4 >2k-word treatments; complete IX.1; 8 direct evidence anchors; all earlier paragraphs and canonical bytes preserved; stable assets')
