#!/usr/bin/env python3
"""Project-level deterministic validation; no paid APIs or external dependencies."""
from pathlib import Path
import json,re,hashlib,sys
R=Path(__file__).resolve().parent.parent
arch=json.loads((R/'data/architecture.json').read_text())
manifest=json.loads((R/'data/content-manifest.json').read_text())
expected=['I','II','III','IV','V','VI','VII','VIII','IX','X']
assert [p['id'] for p in arch['parts']]==expected
ids=set();chapters=0
for p in arch['parts']:
    assert len(p['chapters'])==10,p['id']
    for c in p['chapters']:
        chapters+=1
        assert c['id'].startswith(p['id']+'.')
        assert len(c['subchapters'])==10,c['id']
        for s in c['subchapters']:
            assert s['id'].startswith(c['id']+'.')
            assert s['id'] not in ids
            ids.add(s['id'])
assert len(ids)==1000 and chapters==100
assert arch['counts']['plannedSections']==10*len(ids)
assert arch['counts']['plannedTerminalSubsections']==100*len(ids)
assert len(manifest['articles'])==manifest['count']
assert len({a['id'] for a in manifest['articles']})==manifest['count']
total_words=0;blocks=0
for a in manifest['articles']:
    assert a['id'] in ids
    original=json.loads((R/'data/articles'/f"{a['id']}.json").read_text())
    assert original['title']==a['title']
    assert a['blocks']==len(a['chunks'])==len(original['blocks'])
    words=sum(len(re.findall(r"\b[\w’'-]+\b",p)) for block in original['blocks'] for p in block['paragraphs'])
    assert words==a['wordCount']
    for b,chunk in zip(original['blocks'],a['chunks']):
        assert chunk['id']==b['id']
        path=R/chunk['path'].removeprefix('./')
        assert path.exists(),path
        raw=path.read_bytes(); assert hashlib.sha256(raw).hexdigest()==chunk['sha256']
        assert json.loads(raw)==b
        blocks+=1
    total_words+=words
assert total_words==manifest['sampleWordCount']
assert total_words>=4000
print(f'PASS original structure: {len(arch["parts"])} Parts / {chapters} Chapters / {len(ids)} Subchapters')
print('PASS reserved virtual addresses: 10,000 Section and 100,000 terminal slots')
print(f'PASS corpus integrity: {manifest["count"]} sample articles, {blocks} SHA-256 verified fetchable blocks, {total_words:,} words')

# Batch A exploration metadata derives only from available canonical IDs and source prose.
explore=json.loads((R/'data/explore.json').read_text())
search=json.loads((R/'data/search-index.json').read_text())
assert len(explore['collections'])>=6
assert len({c['slug'] for c in explore['collections']})==len(explore['collections'])
assert all(c['ids'] and len(set(c['ids']))==len(c['ids']) and set(c['ids'])<=ids for c in explore['collections'])
assert search['articleCount']==manifest['count']
assert {a['id'] for a in search['articles']}=={a['id'] for a in manifest['articles']}
for item in search['articles']:
 original=json.loads((R/'data/articles'/f"{item['id']}.json").read_text())
 assert len(item['blocks'])==len(original['blocks'])
 assert [b['text'] for b in item['blocks']]==[' '.join(b['paragraphs']) for b in original['blocks']]
print(f'PASS Batch A exploration: {len(explore["collections"])} canonical trails, full-text index over {len(search["articles"])} articles')
