"""Batch Z frozen authored text, independent baseline and deterministic release audit."""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_corpus import canonical,compile_corpus,WORD_RE
fixture=json.loads((ROOT/'tests/fixtures/batch_z_baseline.json').read_text(encoding='utf-8'))
BASE='f94378fce1e8b6b2425072487a02b68a608acedf'
SNAP='65eda326054f0332e6509fbfbc60c062b50fec71'
assert fixture['baseline_main']==BASE
assert fixture['authored_snapshot']==SNAP
def blob_sha(path):
    raw=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\0'+raw).hexdigest()
def show(ref,path):
    return subprocess.run(['git','show',f'{ref}:{path}'],cwd=ROOT,capture_output=True,check=True).stdout
old=fixture['article_blobs']; canonical_blobs=fixture['canonical_blobs']
assert len(old)==350 and len(canonical_blobs)==15
for path,sha in canonical_blobs.items():
    assert blob_sha(ROOT/path)==sha,('canonical changed',path)
target={f'V.9.{i}' for i in range(1,11)}|{f'VI.10.{i}' for i in range(1,11)}
assert set(fixture['batch_z_blocks'])==target
assert set(fixture['prior_appended'])==set()
titles=canonical()
current={p.stem for p in (ROOT/'data/articles').glob('*.json')}
assert set(old)|target<=current and len(current)>=370
# Preserve every baseline article, its metadata and its entire original passage prefix.
for id,sha in old.items():
    path=ROOT/'data/articles'/f'{id}.json'
    if blob_sha(path)==sha:continue
    original=json.loads(show(BASE,'data/articles/'+id+'.json').decode('utf-8'))
    latest=json.loads(path.read_text(encoding='utf-8'))
    assert latest['blocks'][:len(original['blocks'])]==original['blocks'],('old blocks rewritten',id)
    assert {k:v for k,v in latest.items() if k!='blocks'}=={k:v for k,v in original.items() if k!='blocks'},('old metadata rewritten',id)
words=0; passages=0; anchors=0; prose=[]; per={}
for id in sorted(target):
    a=json.loads((ROOT/'data/articles'/f'{id}.json').read_text(encoding='utf-8'))
    snap=json.loads(show(SNAP,'data/articles/'+id+'.json').decode('utf-8'))
    assert a['id']==id and a['title']==titles[id],('canonical id/title',id)
    assert a['release']=='Z' and len(a['sources'])>=3,id
    assert all(isinstance(s['url'],str) and s['url'].startswith('https://') for s in a['sources'])
    begin=fixture['batch_z_blocks'][id]['prior_blocks']
    end=fixture['batch_z_blocks'][id]['batch_z_end']
    assert begin==0 and len(a['blocks'])>=end and end>=8,id
    assert a['blocks'][:end]==snap['blocks'][:end],('frozen Batch Z passage rewritten',id)
    assert all(b['id']==f'{id}:b{n:02d}' and b.get('sequence',n)==n for n,b in enumerate(a['blocks'][:end],1)),('passage id',id)
    fresh=a['blocks'][begin:end]; passages+=len(fresh)
    cw=0
    for block in fresh:
        assert block.get('title') and block.get('paragraphs'),id
        for paragraph in block['paragraphs']:
            assert isinstance(paragraph,str) and len(paragraph)>=150,('short paragraph',id)
            cw+=len(WORD_RE.findall(paragraph))
            prose.append(paragraph)
        for e in block.get('evidence',[]):
            assert e.get('type') in ('direct','context') and len(e.get('locator',''))>=12,id
            assert len(e.get('claim',''))>=24 and 0<=e['sourceIndex']<len(a['sources']),id
            anchors+=1
    assert cw>=750,('thin narrative article',id,cw)
    per[id]=cw
    words+=cw
normalized=[' '.join(re.findall(r'\\w+',p.casefold())) for p in prose]
assert len(normalized)==len(set(normalized)),'repeated Batch Z prose'
assert 20000<=words<=30000,('new words out of range',words)
assert words==fixture['expected_new_words'],('frozen word-count mismatch',words,fixture['expected_new_words'])
assert passages==fixture['expected_new_passages'],('frozen passages mismatch',passages)
assert anchors>=40,('too few cited evidence anchors',anchors)
aliases=json.loads((ROOT/'content/atlas/search-aliases.json').read_text(encoding='utf-8'))
assert all(id in aliases and len(aliases[id])>=3 for id in target),'missing Korean aliases'
trails=json.loads((ROOT/'data/explore.json').read_text(encoding='utf-8'))['collections']
assert len(trails)>=46
for slug,ch in [('goryeo-mongol-yuan-world-complete','V.9'),('imjin-war-seven-year-conflict-complete','VI.10')]:
    route=next(x for x in trails if x['slug']==slug)
    assert route['ids']==[f'{ch}.{i}' for i in range(1,11)],slug
manifest=json.loads((ROOT/'data/content-manifest.json').read_text(encoding='utf-8'))
assert manifest['count']>=370 and manifest['sampleWordCount']>=345793+words
assert sum(a['blocks'] for a in manifest['articles'])>=2467+passages
if len(current)==370:
    assert manifest['count']==370
    assert manifest['sampleWordCount']==345793+words,('manifest word count',manifest['sampleWordCount'],words)
    assert sum(a['blocks'] for a in manifest['articles'])==2467+passages
first=compile_corpus();second=compile_corpus()
assert second['assets_changed']==0,'nondeterministic rebuild'
assert first['largest_pack']<=24000 and first['largest_shard']<=48000,'unbounded pack or shard'
assets=[p.relative_to(ROOT/'dist').as_posix() for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert assets and all(not x.startswith(('canonical/','content/','scripts/','tests/','data/articles/','data/blocks/')) for x in assets)
print(f'PASS Batch Z exact immutable baseline: +{words:,} words, {passages} passages, 20 new/0 amended existing articles, {anchors} source anchors, two complete Chapters, {len(assets)} safe release assets.')
