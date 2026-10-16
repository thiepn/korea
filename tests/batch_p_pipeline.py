"""Batch P regression audit — immutable baseline, original historical prose, fixed canonical IDs."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts'))
from build_corpus import canonical,compile_corpus,WORD_RE
G=lambda p:hashlib.sha1(b'blob '+str(len(p.read_bytes())).encode()+b'\x00'+p.read_bytes()).hexdigest()
# A Git blob hash includes the NUL byte between the header and its file bytes.
prior=json.loads((R/'tests/fixtures/batch_p_baseline.json').read_text(encoding='utf-8'))
assert prior['base_sha']=='b4c8b70ef112f96fb5e3d9581ed66fc23dd691e2'
assert len(prior['articles'])==183 and len(prior['canonical'])==15
for path,expected in prior['canonical'].items():assert G(R/path)==expected,('canonical changed',path)
written={'I.2.'+str(i) for i in range(3,11)}|{'X.2.'+str(i) for i in (1,3,6,7,8,9,10)}
appended=set(prior['appended_before'])
assert appended=={'I.2.1','I.2.2','X.2.2','X.2.4','X.2.5'}
titles=canonical();delta=0;passages=0;anchors=0
actual={p.stem for p in (R/'data/articles').glob('*.json')}
assert actual-set(prior['articles'])==written,('unexpected new IDs',actual-set(prior['articles']))
assert len(actual)==198
for key,expected in prior['articles'].items():
 path=R/'data/articles'/f'{key}.json'
 assert path.is_file()
 if key not in appended:assert G(path)==expected,('prior article changed',key)
 else:
  previous=prior['appended_before'][key];current=json.loads(path.read_text())
  assert len(current['blocks'])>len(previous['blocks']),key
  assert current['blocks'][:len(previous['blocks'])]==previous['blocks'],('prior blocks changed',key)
  assert {k:v for k,v in current.items() if k!='blocks'}=={k:v for k,v in previous.items() if k!='blocks'},('prior metadata changed',key)
  fresh=current['blocks'][len(previous['blocks']):]
  delta+=sum(len(WORD_RE.findall(p)) for b in fresh for p in b['paragraphs']);passages+=len(fresh)
for key in written:
 d=json.loads((R/'data/articles'/f'{key}.json').read_text())
 assert d['title']==titles[key],('title diverges',key)
 assert len(d['blocks'])>=5,key
 delta+=sum(len(WORD_RE.findall(p)) for b in d['blocks'] for p in b['paragraphs'])
 passages+=len(d['blocks'])
 anchors+=sum(len(b.get('evidence',[])) for b in d['blocks'])
 for b in d['blocks']:
  for item in b.get('evidence',[]):assert 0<=item['sourceIndex']<len(d.get('sources',[])),key
assert 20000<=delta<=30000,('authored word count outside target',delta)
assert anchors>=6,anchors
for chapter in ('I.2','X.2'):
 for i in range(1,11):
  key=f'{chapter}.{i}';d=json.loads((R/'data/articles'/f'{key}.json').read_text())
  assert d['title']==titles[key]
explore=json.loads((R/'data/explore.json').read_text())
assert len(explore['collections'])==26
for slug,chapter in [('paleolithic-korea-complete','I.2'),('contemporary-korean-economy-complete','X.2')]:
 path=next(x for x in explore['collections'] if x['slug']==slug)
 assert path['ids']==[f'{chapter}.{i}' for i in range(1,11)]
alias=json.loads((R/'content/atlas/search-aliases.json').read_text())
for chapter in ('I.2','X.2'):
 assert all(f'{chapter}.{i}' in alias for i in range(1,11))
manifest=json.loads((R/'data/content-manifest.json').read_text())
assert manifest['count']==198
assert manifest['sampleWordCount']==141656+delta,(manifest['sampleWordCount'],delta)
assert manifest['sampleWordCount']>161656
first=compile_corpus();second=compile_corpus()
assert first['largest_pack']<=24000 and first['largest_shard']<=48000
assert second['assets_changed']==0
assert all(not p.relative_to(R/'dist').as_posix().startswith(('canonical/','content/','scripts/','tests/','data/articles/')) for p in (R/'dist').rglob('*') if p.is_file())
print(f'PASS Batch P: {delta:,} new original narrative words, {passages} new passages, 15 new + 5 append-only articles, 2 complete Chapters, {anchors} evidence anchors, 183 prior articles and 15 canonical files preserved')
