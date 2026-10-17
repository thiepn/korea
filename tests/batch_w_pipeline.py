"""Batch W historical regression: immutable source baseline and frozen original prose window."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import canonical,compile_corpus,WORD_RE
fixture=json.loads((ROOT/'tests/fixtures/batch_w_baseline.json').read_text(encoding='utf-8'))
assert fixture['baseline_main']=='6a4365566dec619632c72a6cbba00916966549ea'
def blob_sha(path):
    raw=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
prior=fixture['article_blobs']
assert len(prior)==301 and len(fixture['canonical_blobs'])==15
for path,sha in fixture['canonical_blobs'].items():
    assert blob_sha(ROOT/path)==sha,('canonical file mutated',path)
target={f'VI.1.{i}' for i in range(1,11)}|{f'VII.1.{i}' for i in range(1,11)}
old_targets=set(fixture['prior_appended'])
assert old_targets=={'VI.1.3','VI.1.4','VII.1.1','VII.1.4'}
new=target-old_targets
assert len(new)==16
current={p.stem for p in (ROOT/'data/articles').glob('*.json')}
assert (set(prior)|target)<=current and len(current)>=317
titles=canonical();words=0;passages=0;anchors=0;paragraphs=[]
for id,sha in prior.items():
    path=ROOT/'data/articles'/f'{id}.json'
    if id not in old_targets:
        assert blob_sha(path)==sha,('published article rewritten',id)
    else:
        before=fixture['prior_appended'][id]
        after=json.loads(path.read_text(encoding='utf-8'))
        assert after['blocks'][:len(before['blocks'])]==before['blocks'],('immutable old passage rewritten',id)
        assert {k:v for k,v in after.items() if k!='blocks'}=={k:v for k,v in before.items() if k!='blocks'},('old metadata altered',id)
for id in sorted(target):
    a=json.loads((ROOT/'data/articles'/f'{id}.json').read_text(encoding='utf-8'))
    assert a['id']==id and a['title']==titles[id]
    begin=fixture['batch_w_blocks'][id]['prior_blocks']
    end=fixture['batch_w_blocks'][id]['batch_w_end']
    assert len(a['blocks'])>=end and end>begin,id
    assert all(b['id']==f'{id}:b{n:02d}' for n,b in enumerate(a['blocks'][:end],1)),('passage ID',id)
    fresh=a['blocks'][begin:end]
    passages+=len(fresh)
    for b in fresh:
        assert b.get('title') and b.get('paragraphs'),id
        for p in b['paragraphs']:
            assert isinstance(p,str) and len(p)>80,id
            words+=len(WORD_RE.findall(p));paragraphs.append(p)
    if id in new:
        assert a['release']=='W' and len(fresh)>=7,id
        assert len(a.get('sources',[]))>=2 and all(s.get('url','').startswith('https://') for s in a['sources']),id
        for b in fresh:
            for e in b.get('evidence',[]):
                assert 0<=e['sourceIndex']<len(a['sources']),id
                assert e['type'] in ('direct','context') and len(e['claim'])>=24 and len(e['locator'])>=12,id
                anchors+=1
        assert any(b.get('evidence') for b in fresh),id
normalized=[' '.join(re.findall(r'\w+',p.casefold())) for p in paragraphs]
assert len(normalized)==len(set(normalized)),'duplicate new prose paragraph'
assert 20000<=words<=30000,('Batch W prose out of range',words)
assert passages==fixture['expected_new_passages'],passages
assert anchors>=16,anchors
explore=json.loads((ROOT/'data/explore.json').read_text(encoding='utf-8'))
assert len(explore['collections'])>=40
for slug,ch in [('joseon-founding-1392-complete','VI.1'),('joseon-reconstruction-manchu-complete','VII.1')]:
    path=next(x for x in explore['collections'] if x['slug']==slug)
    assert path['ids']==[f'{ch}.{i}' for i in range(1,11)]
aliases=json.loads((ROOT/'content/atlas/search-aliases.json').read_text(encoding='utf-8'))
assert all(id in aliases and len(aliases[id])>=3 for id in target)
manifest=json.loads((ROOT/'data/content-manifest.json').read_text(encoding='utf-8'))
assert manifest['count']>=317 and manifest['sampleWordCount']>=283787+words
assert sum(x['blocks'] for x in manifest['articles'])>=1954+passages
if len(current)==317:
    assert manifest['sampleWordCount']==283787+words,('unexpected narrative words',words,manifest['sampleWordCount'])
    assert sum(x['blocks'] for x in manifest['articles'])==1954+passages
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0,'nondeterministic content build'
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
assets=[p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert assets and all(not x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in assets)
print(f'PASS Batch W immutable baseline: +{words:,} original words, {passages} passages, 16 new/4 append-only articles, {anchors} evidence anchors, two complete Chapters, {len(assets)} safe release assets.')
