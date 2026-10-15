#!/usr/bin/env python3
"""KOREA v2 publication validation: immutable historical addresses and content hash integrity."""
from pathlib import Path
import hashlib,json,re
from build_corpus import DATA,ROOT,canonical,encode,compile_corpus,digest,WORD_RE
arch=json.loads((DATA/'architecture.json').read_text()); titles=canonical()
assert [p['id'] for p in arch['parts']]==['I','II','III','IV','V','VI','VII','VIII','IX','X']
assert len(titles)==1000 and sum(len(p['chapters']) for p in arch['parts'])==100
assert all(len(p['chapters'])==10 and all(len(c['subchapters'])==10 for c in p['chapters']) for p in arch['parts'])
assert arch['counts']['plannedSections']==10_000 and arch['counts']['plannedTerminalSubsections']==100_000
manifest=json.loads((DATA/'content-manifest.json').read_text());catalog=json.loads((DATA/'search/catalog.json').read_text());shardmap=json.loads((DATA/'search/shard-map.json').read_text())
assert manifest['version']==2 and len(manifest['articles'])==manifest['count']
assert len({a['id'] for a in manifest['articles']})==manifest['count']
assert set(x['id'] for x in catalog['articles'])==set(a['id'] for a in manifest['articles'])
article_words=0;passages=0;seen_packs=set();unique_paths=set()
for entry in manifest['articles']:
 id=entry['id'];assert id in titles and entry['title']==titles[id]
 source=json.loads((DATA/'articles'/f'{id}.json').read_text())
 assert len(source['blocks'])==len(entry['chunks'])==entry['blocks']
 words=sum(len(WORD_RE.findall(p)) for b in source['blocks'] for p in b['paragraphs'])
 assert entry['wordCount']==words,(id,entry['wordCount'],words)
 article_words+=words;passages+=len(source['blocks'])
 for chunk,original in zip(entry['chunks'],source['blocks']):
  assert chunk['id']==original['id'] and chunk['title']==original['title']
  assert digest(encode(original))==chunk['sha256']
  path=ROOT/chunk['pack'].removeprefix('./');raw=path.read_bytes();pack=json.loads(raw)
  assert pack['article']==id and pack['version']==2 and pack['blocks'][chunk['offset']]==original
  unique_paths.add(path)
 for item in entry['packs']:
  path=ROOT/item['path'].removeprefix('./');assert digest(path.read_bytes())==item['sha256']
  assert path.stat().st_size==item['bytes'] and item['bytes']<=24_000+20000
  seen_packs.add(path)
assert article_words==manifest['sampleWordCount']
assert unique_paths==seen_packs==set((DATA/'packs').glob('*.json'))
assert len(seen_packs)<20_000,'Pages free-plan file cap: use R2 after 20k artifacts'
for prefix,meta in shardmap['shards'].items():
 p=ROOT/meta['path'].removeprefix('./');assert p.exists() and digest(p.read_bytes())==meta['sha256']
 content=json.loads(p.read_text());assert content['prefix']==prefix and all(t.startswith(prefix) for t in content['terms'])
 assert all(all(isinstance(pos,list) and len(pos)==2 and 0<=pos[0]<len(manifest['articles']) and 0<=pos[1]<catalog['articles'][pos[0]]['blocks'] for pos in rows) for rows in content['terms'].values())
assert set((DATA/'search/shards').glob('*.json'))=={ROOT/meta['path'].removeprefix('./') for meta in shardmap['shards'].values()}
explore=json.loads((DATA/'explore.json').read_text());assert all(set(c['ids'])<=titles.keys() for c in explore['collections'])
assert compile_corpus(write=False)['words']==article_words
print(f'PASS v1.1: 10 Parts, 100 Chapters, 1,000 canonical topics; 10,000 and 100,000 virtual addresses')
print(f'PASS corpus: {manifest["count"]} articles, {passages} immutable passages, {article_words:,} words, {len(seen_packs)} hash-pinned content packs')
print(f'PASS full-text: {len(shardmap["shards"])} indexed search shards, all hashes verified')
