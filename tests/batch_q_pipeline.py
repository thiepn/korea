"""Batch Q: exact-byte baseline preservation and original narrative publication regression."""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import canonical,compile_corpus,WORD_RE
fixture=json.loads((ROOT/'tests/fixtures/batch_q_baseline.json').read_text(encoding='utf-8'))
assert fixture['baseline_main']=='3dacb68cdf3cadaf999e538f853793c0c381d218'
def blob_sha(path):
    raw=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\x00'+raw).hexdigest()
prior=fixture['article_blobs']
assert len(prior)==198 and len(fixture['canonical_blobs'])==15
for path,sha in fixture['canonical_blobs'].items():
    assert blob_sha(ROOT/path)==sha,('canonical mutation',path)
new={f'I.3.{n}' for n in range(1,11)}|{f'X.3.{n}' for n in range(1,11)}
appended=set(fixture['prior_appended'])
assert appended=={'I.3.3','I.3.4','X.3.1'}
new-=appended
current={f.stem for f in (ROOT/'data/articles').glob('*.json')}
assert current==set(prior)|new and len(current)==215,('unexpected article IDs',len(current))
allowed=canonical();delta=0;new_passages=0;annotations=0;new_text=[]
for id,sha in prior.items():
    path=ROOT/'data/articles'/f'{id}.json'
    if id not in appended:
        assert blob_sha(path)==sha,('published article changed',id)
        continue
    old=fixture['prior_appended'][id];curr=json.loads(path.read_text(encoding='utf-8'))
    assert curr['title']==allowed[id]
    assert curr['blocks'][:len(old['blocks'])]==old['blocks'],('prior passage rewritten',id)
    assert {k:v for k,v in curr.items() if k!='blocks'}=={k:v for k,v in old.items() if k!='blocks'},('prior metadata changed',id)
    fresh=curr['blocks'][len(old['blocks']):]
    assert len(fresh)>=5 and all(fresh),id
    new_passages+=len(fresh)
    for b in fresh:
        new_text.extend(b['paragraphs'])
        delta+=sum(len(WORD_RE.findall(p)) for p in b['paragraphs'])
for id in sorted(new):
    d=json.loads((ROOT/'data/articles'/f'{id}.json').read_text(encoding='utf-8'))
    assert d['id']==id and d['title']==allowed[id],('title or ID changed',id)
    assert d['release']=='Q' and len(d['blocks'])>=5,id
    words=sum(len(WORD_RE.findall(p)) for b in d['blocks'] for p in b['paragraphs'])
    assert words>=520,('underdeveloped new article',id,words)
    delta+=words;new_passages+=len(d['blocks'])
    assert len(d.get('sources',[]))>=2,id
    anchors=[e for b in d['blocks'] for e in b.get('evidence',[])]
    assert anchors,id
    for e in anchors:
        assert 0<=e['sourceIndex']<len(d['sources']),id
        assert e['type'] in ('direct','context'),id
        assert len(e['claim'])>=24 and len(e['locator'])>=12,id
    annotations+=len(anchors)
    new_text.extend(p for b in d['blocks'] for p in b['paragraphs'])
normalized=[' '.join(re.findall(r'\w+',s.casefold())) for s in new_text]
assert len(normalized)==len(set(normalized)), 'duplicate newly written paragraphs'
assert 20000<=delta<=30000,('new narrative word count out of range',delta)
assert annotations>=17,annotations
for chapter in ('I.3','X.3'):
    for i in range(1,11):
        id=f'{chapter}.{i}'
        assert json.loads((ROOT/'data/articles'/f'{id}.json').read_text())['title']==allowed[id],id
explore=json.loads((ROOT/'data/explore.json').read_text())
assert len(explore['collections'])==28,len(explore['collections'])
for slug,chapter in [('neolithic-korea-complete','I.3'),('south-korean-society-complete','X.3')]:
    c=next(c for c in explore['collections'] if c['slug']==slug)
    assert c['ids']==[f'{chapter}.{i}' for i in range(1,11)]
alias=json.loads((ROOT/'content/atlas/search-aliases.json').read_text())
assert all(id in alias and len(alias[id])>=3 for id in new|appended)
manifest=json.loads((ROOT/'data/content-manifest.json').read_text())
assert manifest['count']==215
assert manifest['sampleWordCount']==162166+delta,(manifest['sampleWordCount'],delta)
assert sum(a['blocks'] for a in manifest['articles'])==1077+new_passages
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0,'nondeterministic compiler'
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
assets=[p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert assets and all(not x.startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for x in assets)
print(f'PASS Batch Q exact baseline: +{delta:,} original narrative words, {new_passages} passages, 17 new/3 append-only articles, 17+ anchored sources, 2 complete chapters, {len(assets)} safe public assets.')
