"""Batch Y: immutable published source baseline and frozen original authored prose windows."""
from __future__ import annotations
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import canonical,compile_corpus,WORD_RE
fixture=json.loads((ROOT/'tests/fixtures/batch_y_baseline.json').read_text(encoding='utf-8'))
BASE='74adc154bd38f1541d6ea8d42e1a8e8d243bab05'
SNAP='62ff00e6b6a7505e803e3522432bec7fda22a6e9'
assert fixture['baseline_main']==BASE
def blob_sha(path):
    raw=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def show(ref,path):
    return subprocess.run(['git','show',f'{ref}:{path}'],cwd=ROOT,capture_output=True,check=True).stdout
def authored(id):
    return json.loads(show(SNAP,'data/articles/'+id+'.json').decode('utf-8'))
prior=fixture['article_blobs']
assert len(prior)==334 and len(fixture['canonical_blobs'])==15
for path,sha in fixture['canonical_blobs'].items():
    assert blob_sha(ROOT/path)==sha,('canonical v1.1 mutation',path)
target={f'II.3.{i}' for i in range(1,11)}|{f'V.2.{i}' for i in range(1,11)}
old_targets=set(fixture['prior_appended'])
assert old_targets=={'II.3.2','II.3.4','V.2.3','V.2.5'}
assert target==set(fixture['batch_y_blocks'])
fresh_ids=target-old_targets
assert len(fresh_ids)==16
all_current={p.stem for p in (ROOT/'data/articles').glob('*.json')}
assert set(prior)|target<=all_current and len(all_current)>=350
titles=canonical()
for id,sha in prior.items():
    path=ROOT/'data/articles'/f'{id}.json'
    if blob_sha(path)==sha:continue
    old=fixture['prior_appended'].get(id)
    if old is None: old=json.loads(show(BASE,'data/articles/'+id+'.json').decode('utf-8'))
    curr=json.loads(path.read_text(encoding='utf-8'))
    assert curr['blocks'][:len(old['blocks'])]==old['blocks'],('prior published passage mutated',id)
    assert {k:v for k,v in curr.items() if k!='blocks'}=={k:v for k,v in old.items() if k!='blocks'},('prior article metadata rewritten',id)
word_count=0;passages=0;anchors=0;prose=[]
for id in sorted(target):
    curr=json.loads((ROOT/'data/articles'/f'{id}.json').read_text(encoding='utf-8'))
    snap=authored(id)
    assert curr['id']==id and curr['title']==titles[id]
    begin=fixture['batch_y_blocks'][id]['prior_blocks']
    end=fixture['batch_y_blocks'][id]['batch_y_end']
    assert end>begin and len(curr['blocks'])>=end,id
    assert curr['blocks'][:end]==snap['blocks'][:end],('Batch Y authored prose changed',id)
    assert all(block['id']==f'{id}:b{n:02d}' for n,block in enumerate(curr['blocks'][:end],1)),('passage ID',id)
    fresh=curr['blocks'][begin:end]
    assert len(fresh)>=7,id
    passages+=len(fresh)
    for block in fresh:
        assert block['title'] and block['paragraphs'],id
        for p in block['paragraphs']:
            assert isinstance(p,str) and len(p)>=80,(id,'short prose')
            word_count+=len(WORD_RE.findall(p))
            prose.append(p)
    if id in fresh_ids:
        assert curr['release']=='Y' and len(curr.get('sources',[]))>=2,id
        assert all(s['url'].startswith('https://') for s in curr['sources']),id
        assert sum(len(WORD_RE.findall(p)) for b in fresh for p in b['paragraphs'])>=750,('underdeveloped article',id)
        found=[e for b in fresh for e in b.get('evidence',[])]
        assert len(found)>=1,('no citations',id)
        for evidence in found:
            assert evidence.get('type') in ('direct','context'),id
            assert len(evidence.get('claim',''))>=24 and len(evidence.get('locator',''))>=12,id
            assert 0<=evidence['sourceIndex']<len(curr['sources']),id
        anchors+=len(found)
norm=[' '.join(re.findall(r'\w+',p.casefold())) for p in prose]
assert len(norm)==len(set(norm)),('duplicate Batch Y paragraph')
assert 20000<=word_count<=30000,('original narrative word count',word_count)
assert passages==fixture['expected_new_passages'],passages
assert anchors>=32,anchors
explore=json.loads((ROOT/'data/explore.json').read_text(encoding='utf-8'))
assert len(explore['collections'])>=44
for slug,ch in [('han-commandery-history-complete','II.3'),('goryeo-government-and-law-complete','V.2')]:
    result=next(x for x in explore['collections'] if x['slug']==slug)
    assert result['ids']==[f'{ch}.{i}' for i in range(1,11)]
aliases=json.loads((ROOT/'content/atlas/search-aliases.json').read_text(encoding='utf-8'))
assert all(id in aliases and len(aliases[id])>=3 for id in target)
manifest=json.loads((ROOT/'data/content-manifest.json').read_text(encoding='utf-8'))
assert manifest['count']>=350
assert manifest['sampleWordCount']>=325272+word_count
assert sum(a['blocks'] for a in manifest['articles'])>=2286+passages
if len(all_current)==350:
    assert manifest['count']==350
    assert manifest['sampleWordCount']==325272+word_count,(manifest['sampleWordCount'],word_count)
    assert sum(a['blocks'] for a in manifest['articles'])==2286+passages
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0,'nondeterministic compiler'
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
assets=[p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert assets and all(not x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in assets)
print(f'PASS Batch Y immutable baseline: +{word_count:,} original narrative words, {passages} passages, 16 new/4 append-only articles, {anchors} contextual source anchors, two complete Chapters, {len(assets)} safe release assets.')
